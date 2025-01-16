import os
import kagglehub
import csv
from pathlib import Path
from typing import Any
from PIL import Image
from torch import Tensor
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

from backend.utility.find_mean_std import get_mean_std


class CheXpert(Dataset):
    # Class labels
    CLASSES = [
        "Atelectasis",
        "Consolidation",
        "Infiltration",
        "Pneumothorax",
        "Edema",
        "Emphysema",
        "Fibrosis",
        "Effusion",
        "Pneumonia",
        "Pleural_thickening",
        "Cardiomegaly",
        "Nodule",
        "Mass",
        "Hernia",
        "No Finding",
    ]

    def __init__(
        self,
        root_dir: str,
        train: bool = True,
        transform: Any = None,
    ):
        """
        Initialize the NIH dataset.
        Args:
            root_dir: The directory where the downloader will create the dataset folder.
            train: Whether to use the train or test set.
            transform: The transform to apply to the images.
        """
        # Transform to apply to the images
        self.transform = transform
        # Directory where the dataset folder should be created by the downloader
        self.ROOT_DIR = Path(root_dir)
        # Download the dataset and get the path
        self.DATA_DIR = Path(self._download_dataset())
        # Get the image names to paths mapping
        self.image_to_path = {
            _image.name: _image for _image in self.DATA_DIR.glob("**/*.png")
        }
        # Get the image to label mapping
        self.image_to_label = self._get_image_to_label()
        # Get the list of images to use
        self.inputs_list: list[str] = (
            self._read_listfile(self.DATA_DIR / "train_val_list.txt")
            if train
            else self._read_listfile(self.DATA_DIR / "test_list.txt")
        )

    def __len__(self) -> int:
        """
        Get the length of the dataset.\n
        Returns: The length of the dataset (number of images).
        """
        return len(self.inputs_list)

    def __getitem__(self, idx: int) -> tuple[Any, Tensor]:
        """
        Get an image and its label at the given index.
        Args:
            idx: The index of the image to get.

        Returns: The image with any transformations applied and its label one-hot encoded as a tensor.

        """
        # Get the image name
        image_name = self.inputs_list[idx]
        # Get the image path
        image_path = self.image_to_path[image_name]
        # Read the image
        _image = Image.open(image_path)
        # Apply the transform
        if self.transform:
            _image = self.transform(_image)
        # Get the label
        _label: str = self.image_to_label[image_name]  # a|b|c
        # Split the labels
        labels = _label.split("|")
        # One hot encode the labels
        _label: list[int] = [1 if L in labels else 0 for L in CheXpert.CLASSES]
        return _image, Tensor(_label)

    def _download_dataset(self) -> str:
        """
        Download the NIH dataset from Kaggle. Helper function for the constructor.
        Returns: The path to the downloaded dataset.

        """
        # Set environment variable for kagglehub cache
        os.environ["KAGGLEHUB_CACHE"] = str(self.ROOT_DIR)
        # Download the dataset from kaggle
        _path = kagglehub.dataset_download("nih-chest-xrays/data")
        print(f"Dataset downloaded to: {_path}")
        return _path

    # noinspection PyMethodMayBeStatic
    def _read_listfile(self, listfile: Path) -> list[str]:
        """
        Read the listfile and return the list of images. Helper function for the constructor.
        Args:
            listfile: The path to the listfile.

        Returns: The list of image names.

        """
        with open(listfile, "r") as f:
            return f.read().splitlines()

    def _get_image_to_label(self) -> dict[str, str]:
        """
        Get the mapping of image names to labels. Helper function for the constructor.
        Returns: The mapping of image names to labels.

        """
        label_file = self.DATA_DIR / "Data_Entry_2017.csv"
        with open(label_file, "r") as f:
            reader = csv.DictReader(f)
            return {row["Image Index"]: row["Finding Labels"] for row in reader}

    @staticmethod
    def decode_label(_label: Tensor | list[int]) -> list[str]:
        """
        Decode the one-hot encoded label to the list of classes. Use this to get the class names from the one-hot encoded.\n
        Usage: NIH.decode_label([1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) => ['Atelectasis', 'Infiltration']
        Args:
            _label: The one-hot encoded label as a tensor or list of integers.

        Returns: The list of labels as string names.

        """
        return [CheXpert.CLASSES[idx] for idx, L in enumerate(_label) if L == 1]

    @staticmethod
    def encode_label(_label: list[str]) -> Tensor:
        """
        Encode the list of classes to one-hot encoded label. Use this to encode the class names to one-hot encoded.\n
        Usage: NIH.encode_label(['Atelectasis', 'Infiltration']) => [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        Args:
            _label: The list of labels as string names.

        Returns: The one-hot encoded label as a tensor.

        """
        return Tensor([1 if L in _label else 0 for L in CheXpert.CLASSES])


if __name__ == "__main__":
    # Example usage - root_dir is the backend folder. This makes a datasets folder
    DATA_DIR = "D:\\College\\4ZP6A-capstone\\backend"
    nih = CheXpert(
        root_dir=DATA_DIR,
        transform=transforms.Compose(
            [
                transforms.Grayscale(num_output_channels=3),
                transforms.ToTensor(),
                transforms.Resize((128, 128)),
            ]
        ),
    )
    print(len(nih))
    # Plot first 5 images and labels
    import matplotlib.pyplot as plt

    loader = DataLoader(
        nih, batch_size=256, shuffle=True, num_workers=8, persistent_workers=True
    )
    # fig, axs = plt.subplots(1, 5, figsize=(20, 4))
    # images, labels = next(iter(loader))
    # for i in range(5):
    #     axs[i].imshow(images[i].permute(1, 2, 0))
    #     axs[i].set_title(NIH.decode_label(labels[i]))
    #     axs[i].axis("off")
    # plt.show()
    get_mean_std(loader)
