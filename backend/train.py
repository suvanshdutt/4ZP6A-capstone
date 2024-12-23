from argparse import Namespace, ArgumentParser
from utility.get_model import get_model
from utility.load_data import load_data
from utility.parse_args import parse_arguments
from classes.Classifier import Classifier
from classes.ClearMLLogger import ClearMLLogger
from clearml import Task
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
    RandomGrayscale,
    RandomAffine,
    Grayscale,
)
from torch.utils.data import DataLoader


def train(
    model: Classifier,
    args: Namespace,
    train_loader: DataLoader,
    val_loader: DataLoader,
    task: Task,
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
        monitor="accuracy/val", patience=15, mode="max", min_delta=0.5
    )
    tensorboard_logger = TensorBoardLogger("lightning_logs", name=args.model_name)
    clearml_logger = ClearMLLogger(task, version=tensorboard_logger.version)
    trainer = Trainer(
        accelerator="gpu",
        precision="bf16-mixed",
        max_epochs=args.epochs,
        callbacks=[lr_monitor, early_stopping],
        deterministic=True,
        enable_checkpointing=False,
        logger=[
            tensorboard_logger,
            clearml_logger,
        ],  # Tensorboard and clearML must be used together in this order
    )
    trainer.fit(model=model, train_dataloaders=train_loader, val_dataloaders=val_loader)
    return model, trainer


def main():
    seed_everything(42)
    set_float32_matmul_precision("medium")
    # Parse the arguments
    parser: ArgumentParser = ArgumentParser(
        description="Train script for the NIH dataset. Arguments to this script override the default CONFIG.py file."
    )
    # Get the arguments
    args = parse_arguments(parser)
    # Initialize the ClearML task
    task = Task.init(
        project_name="4ZP6A-capstone", task_name="NIH Training", output_uri=False
    )
    # Load the data with the transformations
    transform: Compose = Compose(
        [
            Resize(
                (args.image_size, args.image_size),
                interpolation=InterpolationMode.BICUBIC,
            ),
            # Convert to 1 channel - some images are 4 channels, some 3 but all grayscale
            Grayscale(num_output_channels=3),
            RandomHorizontalFlip(),
            ToTensor(),
            # Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    train_loader, val_loader, test_loader = load_data(_args=args, _transforms=transform)
    # Initialize the model
    model = get_model(args)
    # Train the model
    model, trainer = train(model, args, train_loader, val_loader, task)
    # Save the model
    trainer.save_checkpoint(
        filepath=args.root_dir + "/models/" + args.model_name + ".ckpt",
        weights_only=False,
    )


if __name__ == "__main__":
    main()
