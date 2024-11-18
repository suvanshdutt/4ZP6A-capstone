import os
import sys
import itertools
import random
import glob
import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, multilabel_confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, auc
import torch
from torch.utils.data import Dataset, DataLoader 
import torch.nn as nn
import torchvision
from torchvision import transforms
import torchvision.models as models
from icecream import ic

from PIL import Image

class NIH_dataset(Dataset):
    '''
    Custom dataset class for the NIH\n
    params:\n
    df: Pandas dataframe containing the data\n
    image_directories: list of directories in string containing the images\n
    transform: torchvision.transforms.transforms. DO NOT PASS transforms.to_tensor() here\n
    target_transform: Not used here\n
    '''
    def __init__(self, df: pd.DataFrame, image_directories: list[str], transform: torchvision.transforms=None, target_transform=None):
        self.df = df
        self.image_dir = image_directories
        self.transform = transform
        self.image_to_path = {os.path.basename(path): path for path in self.image_dir}

    def __len__(self):
        """
        Returns the length of the dataset
        """
        return len(self.df)

    def __getitem__(self, idx: int):
        img_path = self.image_to_path.get(self.df.loc[idx, 'Image Index'])
        label: str = self.df.loc[idx, 'Finding Label']
        img = Image.open(img_path).convert('RGB')
        if self.transform:
            img = self.transform(img)
        return img, label #returns img as tensor matrix, label as string
