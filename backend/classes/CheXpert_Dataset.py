import pandas as pd
import numpy as np
from pathlib import Path
from typing import Any
from PIL import Image
from torch import Tensor, torch
from torch.utils.data import Dataset
import tqdm


class CheXpert(Dataset):
    # Class labels
    CLASSES = [
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
        "No Finding",
    ]

    POS_CLASSES = [
        "Atelectasis",
        "Edema",
        
    ]

    NEG_CLASSES = [
        "Cardiomegaly",
        "Consolidation",
        "Enlarged Cardiomediastinum",
        "Fracture",
        "Lung Lesion",
        "Lung Opacity",
        "No Finding",
        "Pleural Effusion",
        "Pleural Other",
        "Pneumonia",
        "Pneumothorax",
        "Support Devices",
    ]

    def __init__(self, root_dir: str = ".", train: bool = True, transform: Any = None):
        """Initialize the CheXpert dataset.

        Args:
            root (str, optional): root directory. Defaults to ".".
            train (bool, optional): Whether to load training data. Defaults to True.
            transform (Any, optional): Image transforms. Defaults to None.
        """
        self.ROOT_DIR = Path(root_dir)
        self.DATA_DIR: Path = Path(self.ROOT_DIR) / "CheXpert"
        self.train = train
        self.transform = transform
        self.image_paths, self.labels = self._get_image_paths_labels()
        self.image_paths = np.array(self.image_paths)
        self.labels = np.array(self.labels)


    def __len__(self):
        """Get the length of the dataset.

        Returns:
            Int: The length of the dataset (number of images).
        """
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> tuple[Image.Image, Tensor]:
        """Get the image and label at the given index.

        Args:
            idx (int): The index of the image.

        Returns:
            tuple[Image.Image, Tensor]: The image and label at the given index.
        """
        image_path = self.image_paths[idx]
        image = Image.open(image_path)
        if self.transform:
            image = self.transform(image)

        return image, self.labels[idx]

    def _read_listfile(self, listfile: Path) -> tuple[list[str], list[Tensor]]:
        """Read the listfile and return the image paths and labels.

        Args:
            listfile (Path): csv file containing the image paths and labels.

        Returns:
            tuple[list[str], list[Tensor]]: The image paths and corresponding labels.
        """
        data = pd.read_csv(listfile)
        # training on only frontal x-rays
        # data = data[data["Frontal/Lateral"] == "Frontal"]

        images_paths: list[str] = data["Path"].tolist()

        images_paths = list(
            map(
                lambda s: s.replace("CheXpert-v1.0/train/", "").replace(
                    "CheXpert-v1.0/valid/", ""
                ),
                images_paths,
            )
        )
        images_paths = self._generate_full_patient_paths(images_paths)

        # Assigning uncertain labels according to each class's performance.
        labels = data[CheXpert.CLASSES].replace(-1, 0).fillna(0)
        labels.update((data[CheXpert.POS_CLASSES].replace(-1, 1).fillna(0)))
        labels = labels.values
        labels = [torch.from_numpy(row) for row in labels]

        return images_paths, labels

    def _generate_full_patient_paths(self, paths: list[str]) -> list[str]:
        """Generate the full path to the images based on the patient id.

        Args:
            paths (list[str]): The list of incomplete image paths.

        Returns:
            list[str]: The list of full image paths.
        """

        for p, path in enumerate(paths):
            patient_id = int(path[7:12])
            if patient_id < 21514:
                paths[p] = (
                    str(self.DATA_DIR.absolute())
                    + "/CheXpert-v1.0 batch 2 (train 1)/"
                    + path
                )
            elif patient_id < 43018:
                paths[p] = (
                    str(self.DATA_DIR.absolute())
                    + "/CheXpert-v1.0 batch 3 (train 2)/"
                    + path
                )
            elif patient_id < 64541:
                paths[p] = (
                    str(self.DATA_DIR.absolute())
                    + "/CheXpert-v1.0 batch 4 (train 3)/"
                    + path
                )
            else:
                paths[p] = (
                    str(self.DATA_DIR.absolute())
                    + "/CheXpert-v1.0 batch 1 (validate & csv)/valid/"
                    + path
                )

        return paths

    def _get_image_paths_labels(self) -> tuple[list[str], list[Tensor]]:
        """Get the image paths and labels from the csv file.

        Returns:
            tuple[list[str], list[Tensor]]: The image paths and corresponding labels.
        """
        if self.train:
            # using only binary labels
            listfile = self.DATA_DIR / "train_visualCheXbert.csv"  #use train_cheXbert.csv for uncertain labels
        else:
            listfile = (
                self.DATA_DIR
                / "CheXpert-v1.0 batch 1 (validate & csv)"
                / "valid.csv"
            )

        return self._read_listfile(listfile)

    @staticmethod
    def get_decoded(encoded: Tensor) -> list[str]:
        """Return the diseases from the one-hot encoded tensor.

        Args:
            encoded (Tensor): The one-hot encoded tensor.

        Returns:
            list[str]: The list of diseases.
        """

        diseases = []
        for i, disease in enumerate(encoded):
            if disease == 1:
                diseases.append(CheXpert.CLASSES[i])

        return diseases

    @staticmethod
    def get_encoded(diseases: list[str]) -> Tensor:
        """Return the one-hot encoded tensor from the list of diseases.

        Args:
            diseases (list[str]): The list of diseases.

        Returns:
            Tensor: The one-hot encoded tensor.
        """

        encoded = torch.zeros(len(CheXpert.CLASSES))
        for disease in diseases:
            encoded[CheXpert.CLASSES.index(disease)] = 1

        return encoded


if __name__ == "__main__":
    dataset = CheXpert(root_dir="D:/datasets/", train=True)

    modes = set()
    for i in tqdm.tqdm(range(len(dataset))):
        img, label = dataset[i]
        modes.add(img.mode)
        if i % 10000 == 0:
            print(modes)
