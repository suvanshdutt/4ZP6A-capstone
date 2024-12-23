import argparse
import sys

import numpy as np
import timm
import timm.optim
import torch
import torch.optim
from argparse import Namespace, ArgumentParser
from utility.parse_args import parse_arguments
from typing import Any, Optional, Union, Dict, Literal
from clearml import Task
from lightning import LightningModule, seed_everything, Trainer
from lightning.pytorch.callbacks import LearningRateMonitor, EarlyStopping
from lightning.pytorch.loggers import Logger, TensorBoardLogger
from torchmetrics.functional import accuracy, confusion_matrix, f1_score
from matplotlib import pyplot as plt
from torch import nn, Tensor, set_float32_matmul_precision
from torchvision.datasets import CIFAR100
from torchvision.transforms import (
    Compose,
    ToTensor,
    InterpolationMode,
    Normalize,
    Resize,
    RandomHorizontalFlip,
    RandomGrayscale,
    RandomAffine,
)
from torch.utils.data import DataLoader, random_split


def main():
    # Parse the arguments
    parser: ArgumentParser = ArgumentParser(
        description="Train script for the NIH dataset. Arguments to this script override the default CONFIG.py file."
    )
    args = parse_arguments(parser)
    print(args.epochs)


if __name__ == "__main__":
    main()
