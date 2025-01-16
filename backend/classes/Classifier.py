import numpy as np
import timm
import timm.optim
import torch
from argparse import Namespace
from lightning import LightningModule
from torch import Tensor, nn
from torchmetrics.functional import accuracy, confusion_matrix, f1_score
from typing import Any, Literal
from backend.classes.ClearMLLogger import ClearMLLogger


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

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch: Any, batch_idx: int):
        metrics = self._calculate_metrics(batch)
        self.log("loss/train", metrics["loss"], on_epoch=True, on_step=False)
        self.log("accuracy/train", metrics["accuracy"], on_epoch=True, on_step=False)
        return metrics["loss"]

    def validation_step(self, batch: Any, batch_idx: int):
        metrics = self._calculate_metrics(batch)
        self.log("loss/val", metrics["loss"], on_epoch=True)
        self.log("accuracy/val", metrics["accuracy"], on_epoch=True)
        return metrics["loss"]

    def test_step(self, batch: Any, batch_idx: int):
        metrics = self._calculate_metrics(batch)
        self.log("test loss", metrics["loss"], on_epoch=True)
        self.log("test accuracy", metrics["accuracy"], on_epoch=True)
        self.log("test f1 score", metrics["f1_score"], on_epoch=True)
        # noinspection all
        clearml_logger: ClearMLLogger = self.loggers[1]
        # noinspection PyUnresolvedReferences
        clearml_logger.report_confusion_matrix(
            "Confusion Matrix",
            "test",
            iteration=batch_idx,
            matrix=metrics["confusion"].numpy(force=True),
        )
        return metrics["loss"]

    def configure_optimizers(self) -> dict[str, dict[str, Any]]:
        match self.optimizer.lower():
            case "sgd-torch":
                optimizer = torch.optim.SGD(
                    params=self.parameters(),
                    lr=self.lr,
                    weight_decay=self.weight_decay,
                    momentum=self.momentum,
                )
            case _:
                optimizer = timm.optim.create_optimizer_v2(
                    model_or_params=self.parameters(),
                    opt=self.optimizer,
                    lr=self.lr,
                    weight_decay=self.weight_decay,
                    momentum=self.momentum,
                )
        # Scheduler
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode="max", factor=0.5, patience=5, threshold=0.001
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
        acc = accuracy(
            preds=probabilities,
            target=_labels,
            num_classes=self.num_classes,
            average="weighted",
            task="multilabel",
            num_labels=self.num_classes,
        )
        confusion = confusion_matrix(
            preds=probabilities,
            target=_labels,
            num_classes=self.num_classes,
            task="multiclass",
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
        return {
            "loss": loss,
            "accuracy": acc * 100,
            "confusion": confusion,
            "f1_score": f1,
        }
