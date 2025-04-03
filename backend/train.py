from argparse import Namespace, ArgumentParser
from pathlib import Path
import torch
from utility.get_model import get_model
from utility.load_data import load_data
from utility.parse_args import parse_arguments
from classes.Classifier import Classifier
#from classes.ClearMLLogger import ClearMLLogger
#from clearml import Task
from lightning import LightningModule, seed_everything, Trainer
from lightning.pytorch.callbacks import LearningRateMonitor, EarlyStopping
from lightning.pytorch.loggers import Logger, TensorBoardLogger
from torch import nn, Tensor, set_float32_matmul_precision
from torchvision.transforms import (
    Compose,
    ToTensor,
    InterpolationMode,
    Normalize,
    Resize,
    RandomHorizontalFlip,
    RandomAffine,
    ColorJitter,
    Grayscale,
)
from torch.utils.data import DataLoader
import matplotlib


def train(
    model: Classifier,
    args: Namespace,
    train_loader: DataLoader,
    val_loader: DataLoader,
    # task: Task,
) -> tuple[Classifier, Trainer]:
    """
    Trains the given model using the provided data loaders and task.

    Args:
        model (Classifier): The model to be trained.
        args (Namespace): The command-line arguments containing training parameters.
        train_loader (DataLoader): The DataLoader for the training data.
        val_loader (DataLoader): The DataLoader for the validation data.
        task (Task): The ClearML task for logging and tracking.

    Returns:
        tuple[Classifier, Trainer]: A tuple containing the trained model and the Trainer object.
    """
    lr_monitor = LearningRateMonitor(logging_interval="epoch")
    early_stopping = EarlyStopping(
        monitor="accuracy/val", patience=5, mode="max", min_delta=0.0005
    )
    tensorboard_logger = TensorBoardLogger("lightning_logs", name=args.model_name)
    #clearml_logger = ClearMLLogger(task, version=tensorboard_logger.version)
    trainer = Trainer(
        accelerator="gpu",
        devices=args.devices,
        num_nodes=1,
        strategy='ddp', # ddp_find_unused_parameters_True
        precision="bf16-mixed",
        max_epochs=args.epochs,
        callbacks=[lr_monitor, early_stopping],
        deterministic=False,
        use_distributed_sampler=False,
        enable_checkpointing=False,
        logger=[
            tensorboard_logger,
            #clearml_logger,
        ],  # Tensorboard and clearML must be used together in this order
    )
    
    trainer.fit(model=model, train_dataloaders=train_loader, val_dataloaders=val_loader)
    return model, trainer


def main():
    seed_everything(42)
    set_float32_matmul_precision("medium")
    # Parse the arguments
    parser: ArgumentParser = ArgumentParser(
        description="Train script for the CheXpert dataset. Arguments to this script override the default CONFIG.py file."
    )
    # Get the arguments
    args = parse_arguments(parser)
    # Initialize the ClearML task
    # task = Task.init(
    #     project_name="4ZP6A-capstone",
    #     task_name="CheXpert Training",
    #     output_uri=False,
    #     reuse_last_task_id=False,
    # )
    # Load the data with the transformations
    transform: Compose = Compose(
        [
            # Convert to 1 channel
            Grayscale(num_output_channels=3),
            Resize(
                (args.image_size, args.image_size),
                interpolation=InterpolationMode.BICUBIC,
            ),
            RandomHorizontalFlip(),
            RandomAffine(degrees=30, translate=(0.30,0.30), scale=(0.70,1.30)),
            ColorJitter(brightness=0.30, contrast=0.30),
            ToTensor(),
            Normalize(
                mean=[0.5057019, 0.5057019, 0.5057019],
                std=[0.24987267, 0.24987267, 0.24987267],
            ),
        ]
    )
    train_loader, val_loader, test_loader = load_data(_args=args, _transforms=transform)
    # Initialize the model
    model = get_model(args)
    # Train the model
    model, trainer = train(model, args, train_loader, val_loader)
    matplotlib.use('Agg')
    # Save the model
    trainer.save_checkpoint(
        Path(args.root_dir) / f"{args.model_name}.ckpt",
        weights_only=False,
    )
    # Save the model state_dict
    torch.save(model.state_dict(), Path(args.root_dir) / f"{args.model_name}.pth")
    # Test the model
    trainer._accelerator_connector._devices_flag = 1
    trainer.test(model=model, dataloaders=test_loader)


if __name__ == "__main__":
    main()
