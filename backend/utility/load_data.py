from argparse import Namespace
from torch.utils.data import DataLoader, random_split
from torchvision.transforms import Compose
from backend.classes.NIH_Dataset import NIH


def load_data(
    _args: Namespace, _transforms: Compose = None
) -> tuple[DataLoader, DataLoader, DataLoader]:
    """
    Loads the data and splits it into training, validation, and test sets.

    Args:
        _args (Namespace): The command-line arguments containing data loading parameters.
        _transforms (Compose, optional): The transformations to apply to the dataset. Defaults to None.

    Returns:
        tuple[DataLoader, DataLoader, DataLoader]: A tuple containing the DataLoaders for the training, validation, and test sets.
    """

    # Load the data
    train_val_dataset: NIH = NIH(
        root_dir=_args.root_dir, train=True, transform=_transforms
    )
    test_dataset: NIH = NIH(root_dir=_args.root_dir, train=False, transform=_transforms)
    # Split the training dataset into train and validation
    train_dataset, val_dataset, _ = random_split(
        train_val_dataset,
        lengths=[
            _args.train_size,
            _args.val_size,
            int(1 - _args.train_size - _args.val_size),
        ],
    )
    print(f"Training dataset size: {len(train_dataset)}")
    print(f"Validation dataset size: {len(val_dataset)}")
    print(f"Test dataset size: {len(test_dataset)}")

    return (
        DataLoader(
            train_dataset,
            batch_size=_args.batch_size,
            shuffle=True,
            num_workers=_args.num_workers,
            persistent_workers=True,
        ),
        DataLoader(
            val_dataset,
            batch_size=_args.batch_size,
            shuffle=False,
            num_workers=_args.num_workers,
            persistent_workers=True,
        ),
        DataLoader(
            test_dataset,
            batch_size=_args.batch_size,
            shuffle=False,
            num_workers=_args.num_workers,
            persistent_workers=True,
        ),
    )
