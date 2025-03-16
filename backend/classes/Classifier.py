import numpy as np
import timm
import timm.optim
import torch
from argparse import Namespace
from lightning import LightningModule
from torch import Tensor, nn
from torchmetrics.functional import accuracy, confusion_matrix, f1_score, auroc, precision_recall_curve, precision, recall
from torcheval.metrics.functional.aggregation.auc import auc
from typing import Any, Literal
#from backend.classes.ClearMLLogger import ClearMLLogger
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score
import numpy as np


class FocalLoss(nn.Module):
    def __init__(self, alpha=0.25, gamma=2.0, reduction="mean"):
        """
        Args:
            alpha (float): Weighting factor for the positive class (helps with class imbalance).
            gamma (float): Focusing parameter (higher values focus more on hard examples).
            reduction (str): "mean" for averaging the loss, "sum" for sum of losses, or "none" for no reduction.
        """
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction
        self.bce = nn.BCEWithLogitsLoss(reduction="none") 

    def forward(self, logits, targets):
        """
        Args:
            logits: Raw output from the model before activation (i.e., before sigmoid).
            targets: Ground truth labels (same shape as logits).
        
        Returns:
            Focal loss value.
        """
        # Compute binary cross-entropy loss
        bce_loss = self.bce(logits, targets)

        # Compute probability (sigmoid of logits)
        probs = torch.sigmoid(logits)
        p_t = probs * targets + (1 - probs) * (1 - targets)  # p_t = p for positive, 1-p for negative

        # Compute focal weight
        focal_weight = self.alpha * targets + (1 - self.alpha) * (1 - targets)
        focal_weight *= (1 - p_t) ** self.gamma  # (1 - p_t)^gamma

        # Apply focal weight to BCE loss
        focal_loss = focal_weight * bce_loss

        if self.reduction == "mean":
            return focal_loss.mean()
        elif self.reduction == "sum":
            return focal_loss.sum()
        else:
            return focal_loss  # Return un-reduced loss

class Classifier(LightningModule):
    def __init__(self, model: nn.Module, args: Namespace):
        """
        Initializes the Classifier class.
        Args:
            model: The model to be used for classification.
            args: The arguments passed to the script or the default arguments in CONFIG.py.
        """
        super(Classifier, self).__init__()
        self.clearml_logger = None
        self.model = model
        self.lr = args.lr
        self.weight_decay = args.weight_decay
        self.momentum = args.momentum
        self.optimizer = args.optimizer
        self.num_classes = args.num_classes

        self.class_names = [
            "Enlarged Cardiomediastinum", 
            "Cardiomegaly", 
            "Lung Opacity",
            "Lung Lesion", 
            "Edema", 
            "Consolidation", 
            "Pneumonia", 
            "Atelectasis",
            "Pneumothorax", 
            "Pleural Effusion", 
            "Pleural Other", 
            "Fracture",
            "Support Devices", 
            "No Finding"
        ]
        
        # Training history storage
        self.train_losses = []
        self.train_accs = []
        self.val_losses = []
        self.val_accs = []
        
        self.roc = []

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch: Any, batch_idx: int):
        metrics = self._calculate_metrics(batch)
        self.log("loss/train", metrics["loss"], on_epoch=True, on_step=False, sync_dist=True)
        self.log("accuracy/train", metrics["accuracy"], on_epoch=True, on_step=False, sync_dist=True)
        return metrics["loss"]
    
    def on_train_epoch_end(self):
        """Print training metrics after each epoch"""

        avg_loss = self.trainer.callback_metrics.get("loss/train")
        avg_acc = self.trainer.callback_metrics.get("accuracy/train")

        if avg_loss is not None:
            self.train_losses.append(avg_loss.cpu().item())
        if avg_acc is not None:
            self.train_accs.append(avg_acc.cpu().item())

        print(f"\nEpoch {self.current_epoch+1} - "
              f"Train Loss: {avg_loss:.4f}, "
              f"Train Acc: {avg_acc:.2f}%")

    def validation_step(self, batch: Any, batch_idx: int):
        metrics = self._calculate_metrics(batch)
        self.log("loss/val", metrics["loss"], on_epoch=True, sync_dist=True)
        self.log("accuracy/val", metrics["accuracy"], on_epoch=True, sync_dist=True)
        return metrics["loss"]
    
    def on_validation_epoch_end(self):
        """Print validation metrics after each epoch"""

        avg_loss = self.trainer.callback_metrics.get("loss/val")
        avg_acc = self.trainer.callback_metrics.get("accuracy/val")

        if avg_loss is not None:
            self.val_losses.append(avg_loss.cpu().item())
        if avg_acc is not None:
            self.val_accs.append(avg_acc.cpu().item())

        print(f"\nEpoch {self.current_epoch+1} - "
              f"Val Loss: {avg_loss:.4f}, "
              f"Val Acc: {avg_acc:.2f}%")
        
    def on_train_end(self):
        """Save training metrics plot at end of training"""

        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(self.train_losses, label='Train')
        plt.plot(self.val_losses, label='Validation')
        plt.title('Loss Curve')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(self.train_accs, label='Train')
        plt.plot(self.val_accs, label='Validation')
        plt.title('Accuracy Curve')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()

        plt.tight_layout()
        plt.savefig('training_metrics.png')
        plt.close()

    def test_step(self, batch: Any, batch_idx: int):
        metrics = self._calculate_metrics(batch)
        self.log("test loss", metrics["loss"], on_epoch=True, sync_dist=True)
        self.log("test accuracy", metrics["accuracy"], on_epoch=True, sync_dist=True)
        self.log("test precision", metrics["precision"], on_epoch=True, sync_dist=True)
        self.log("test recall", metrics["recall"], on_epoch=True, sync_dist=True)
        self.log("test f1 score", metrics["f1_score"], on_epoch=True, sync_dist=True)
        self.log("test roc1:", metrics["roc1"], on_epoch=True, sync_dist=True)
        self.log("test auprc:", metrics["auprc"], on_epoch=True, sync_dist=True)
        # # noinspection all
        # clearml_logger: ClearMLLogger = self.loggers[1]
        # # noinspection PyUnresolvedReferences
        # clearml_logger.report_confusion_matrix(
        #     "Confusion Matrix",
        #     "test",
        #     iteration=batch_idx,
        #     matrix=metrics["confusion"].numpy(force=True),
        # )

        # Return predictions and labels for ROC AUC calculation
        
        self.roc.append({
            "loss": metrics["loss"],
            "probabilities": metrics["probabilities"],
            "labels": metrics["labels"]
        })

        return {
            "loss": metrics["loss"],
            "probabilities": metrics["probabilities"],
            "labels": metrics["labels"]
        }
    

    def on_test_epoch_end(self):

        outputs = self.roc
        # Concatenate all batches
        all_probs = torch.cat([x["probabilities"] for x in outputs]).cpu().to(torch.float32).numpy()
        all_labels = torch.cat([x["labels"] for x in outputs]).cpu().numpy()
        
        # Calculate ROC AUC for each disease
        roc_auc_scores = []
        for i in range(self.num_classes):
            try:
                score = roc_auc_score(all_labels[:, i], all_probs[:, i])
                self.log(f"roc_auc/{self.class_names[i]}", score, sync_dist=True)
                roc_auc_scores.append(score)
                
            except ValueError as e:
                print(f"Could not calculate ROC AUC for {self.class_names[i]}: {e}")
                continue
        
        # Calculate weighted average ROC AUC
        # Using the number of positive samples for each class as weights
        class_weights = all_labels.sum(axis=0)
        weighted_avg_roc_auc = np.average(roc_auc_scores, weights=class_weights)
        
        self.log("test_weighted_roc_auc", weighted_avg_roc_auc, sync_dist=True)
    

    def configure_optimizers(self) -> dict[str, dict[str, Any]]:
        if self.optimizer.lower() == "sgd-torch":
            optimizer = torch.optim.SGD(
                params=self.parameters(),
                lr=self.lr,
                weight_decay=self.weight_decay,
                momentum=self.momentum,
            )
        else:
            optimizer = timm.optim.create_optimizer_v2(
                model_or_params=self.parameters(),
                opt=self.optimizer,
                lr=self.lr,
                weight_decay=self.weight_decay,
                momentum=self.momentum,
            )
        # Scheduler
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode="max", factor=0.1, patience=5, threshold=0.001, min_lr=0.0000001
        )
        scheduler_config = {
            "scheduler": scheduler,
            "monitor": "accuracy/val",
            "interval": "epoch",  # "step" or "epoch"
            "name": "Current LR",
        }
        return {"optimizer": optimizer, "lr_scheduler": scheduler_config}

    def _calculate_metrics(
        self, batch
    ) -> dict[Literal["loss", "accuracy", "confusion", "f1_score"], Tensor]:
        """
        Calculate the metrics for the given batch.
        Args:
            batch: The batch of data to calculate the metrics for.

        Returns: The metrics for the given batch as a dictionary.

        """
        _images, _labels = batch
        logits: Tensor = self(_images)
        probabilities = torch.sigmoid(logits)

        loss = nn.functional.binary_cross_entropy_with_logits(logits, _labels)

        # Other loss function options:

        # focal_loss_fn = FocalLoss(alpha=0.25, gamma=2)
        # loss = 0.5 * nn.functional.binary_cross_entropy_with_logits(logits, _labels) + \
        #        0.5 * focal_loss_fn(logits, _labels)


        acc = accuracy(
            preds=probabilities,
            target=_labels,
            num_classes=self.num_classes,
            average="weighted",
            task="multilabel",
            num_labels=self.num_classes,
        )
        # confusion = confusion_matrix(
        #     preds=probabilities,
        #     target=_labels,
        #     num_classes=self.num_classes,
        #     task="multiclass",
        #     num_labels=self.num_classes,
        # )
        # Precision
        precision_score = precision(
            preds=probabilities,
            target=_labels,
            num_classes=self.num_classes,
            average="weighted",
            task="multilabel",
            num_labels=self.num_classes,
        )

        # Recall
        recall_score = recall(
            preds=probabilities,
            target=_labels,
            num_classes=self.num_classes,
            average="weighted",
            task="multilabel",
            num_labels=self.num_classes,
        )

        f1 = f1_score(
            preds=probabilities,
            target=_labels,
            num_classes=self.num_classes,
            average="weighted",
            task="multilabel",
            num_labels=self.num_classes,
        )
        roc1 = auroc(
            preds=probabilities,
            target=_labels.to(torch.int64),
            num_classes=self.num_classes,
            average="weighted",
            task="multilabel",
            num_labels=self.num_classes,
        )
        precisions, recalls, thresholds = precision_recall_curve(
            preds=probabilities, 
            target=_labels.to(torch.int64), 
            num_classes=self.num_classes,
            average="weighted",
            task="multilabel",
            num_labels=self.num_classes,
        )
        precisions = torch.cat(precisions).to(torch.float32)
        recalls = torch.cat(recalls).to(torch.float32)
        auprc = auc(recalls, precisions, reorder=True)
        return {
            "loss": loss,
            "accuracy": acc * 100,
            # "confusion": confusion,
            "f1_score": f1,
            "auprc": auprc,
            "roc1": roc1,
            "precision": precision_score,
            "recall": recall_score,
            "probabilities": probabilities,
            "labels": _labels
        }
