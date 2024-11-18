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

# Class for metrics


class Metrics:
    def __init__(self, test_mode: bool = False):
        # Lists for storing the metrics
        self.test_mode = test_mode
        self.y_true = None
        self.y_pred = None
        self.losses = []
        self.accuracy = []
        self.precision = []
        self.recall = []
        self.f1 = []
        self.roc_auc = []
        self.tn, self.fp, self.fn, self.tp = [], [], [], []

    def compute(self, y_true: torch.tensor, y_pred: torch.tensor, loss: torch.tensor = None):
        self.y_true = y_true
        self.y_pred = y_pred
        if loss:
            self._compute(loss)
        else:
            self._compute()

    def _compute(self, loss: torch.tensor = None):
        # Accuracy
        self.accuracy.append(accuracy_score(self.y_true, self.y_pred))
        # Precision
        self.precision.append(precision_score(
            self.y_true, self.y_pred, average='macro', zero_division=0))
        # Recall
        self.recall.append(recall_score(
            self.y_true, self.y_pred, average='macro', zero_division=0))
        # F1 Score
        self.f1.append(f1_score(self.y_true, self.y_pred,
                       average='macro', zero_division=0))
        # ROC AUC
        # self.roc_auc.append(roc_auc_score(self.y_true, self.y_pred, average='macro', multi_class="ovo"))

        # Confusion Matrix
        conf_matrices = multilabel_confusion_matrix(self.y_true, self.y_pred)
        # Summing the confusion matrices
        conf_matrix = conf_matrices.sum(axis=0)
        # Getting the values
        tn, fp, fn, tp = conf_matrix.ravel()
        self.tn.append(tn)
        self.fp.append(fp)
        self.fn.append(fn)
        self.tp.append(tp)
        self.losses.append(loss.item()) if loss else None

    def process_by_groups(self, group_size: int) -> None:
        '''
        Process the metrics by groups. Finds the mean of the metrics for each group\n
        '''
        self.losses = list(map(np.mean, np.array_split(
            self.losses, np.arange(group_size, len(self.losses), group_size))))
        self.accuracy = list(map(np.mean, np.array_split(
            self.accuracy, np.arange(group_size, len(self.accuracy), group_size))))
        self.precision = list(map(np.mean, np.array_split(
            self.precision, np.arange(group_size, len(self.precision), group_size))))
        self.recall = list(map(np.mean, np.array_split(
            self.recall, np.arange(group_size, len(self.recall), group_size))))
        self.f1 = list(map(np.mean, np.array_split(
            self.f1, np.arange(group_size, len(self.f1), group_size))))
        self.tp = list(map(np.mean, np.array_split(
            self.tp, np.arange(group_size, len(self.tp), group_size))))
        self.tn = list(map(np.mean, np.array_split(
            self.tn, np.arange(group_size, len(self.tn), group_size))))
        self.fp = list(map(np.mean, np.array_split(
            self.fp, np.arange(group_size, len(self.fp), group_size))))
        self.fn = list(map(np.mean, np.array_split(
            self.fn, np.arange(group_size, len(self.fn), group_size))))

    def __str__(self):
        if self.test_mode:
            return f"""            Avg loss: {np.mean(self.losses):.4f}
                    Avg accuracy: {np.mean(self.accuracy):.4f}
                    Avg precision: {np.mean(self.precision):.4f}
                    Avg recall: {np.mean(self.recall):.4f}
                    Avg f1: {np.mean(self.f1):.4f}"""
        else:
            f"""            Final loss: {self.losses[-1]:.4f}
                    Final accuracy: {self.accuracy[-1]:.4f}
                    Final precision: {self.precision[-1]:.4f}
                    Final recall: {self.recall[-1]:.4f}
                    Final f1: {self.f1[-1]:.4f}"""
            # Final roc_auc: {self.roc_auc[-1]:.4f}

    def plot(self, save: bool = False, path: str = ".", show: bool = False):
        fig, ax = plt.subplots(2, 2, figsize=(16, 12))
        # Loss
        ax[0, 0].plot(self.losses)
        ax[0, 0].set_title('Loss')
        # Accuracy
        ax[0, 1].plot(self.accuracy)
        ax[0, 1].set_title('Accuracy')
        # Precision
        ax[1, 0].plot(self.precision)
        ax[1, 0].set_title('Precision')
        # Recall
        ax[1, 1].plot(self.recall)
        ax[1, 1].set_title('Recall')

        if show:
            plt.show()
        if save:
            plt.savefig(f"{path}/metrics.png")
