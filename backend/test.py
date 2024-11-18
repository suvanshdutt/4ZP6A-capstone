#!/usr/bin/env python
# coding: utf-8

# In[9]:


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
import torch
from torch.utils.data import Dataset, DataLoader 
import torch.nn as nn
import torchvision
from torchvision import transforms
import torchvision.models as models
from icecream import ic

from PIL import Image
from classes.NIH_dataset_class import NIH_dataset
from classes.Metrics_class import Metrics


# In[ ]:


def test(
    model_path: str,
    use_saved_dataframe: bool = True,
    test_df_path: str = 'test_df.pkl',
    dataset_dir: str = './dataset',
    test_split_ratio: float = 0.1,
    batch_size: int = 32
):
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    labels_csv = 'Data_Entry_2017.csv'
    criterion = nn.CrossEntropyLoss()
    # Load or split test data
    if use_saved_dataframe:
        print(f"Loading test DataFrame from {test_df_path}")
        test_df = pd.read_pickle(test_df_path)
    else:
        print("Splitting dataset...")
        labels = pd.read_csv(os.path.join(dataset_dir, labels_csv))
        labels_expanded = labels.copy()
        labels_expanded['Finding Label'] = labels_expanded['Finding Labels'].str.split('|')
        labels_expanded['Id'] = list(zip(labels_expanded['Patient ID'], labels_expanded['Follow-up #']))
        labels_expanded = labels_expanded.explode('Finding Label')
        data = labels_expanded[['Id', 'Image Index', 'Finding Label', 'Patient Age', 'Patient Gender', 'View Position']].copy()
        unique_diseases = data['Finding Label'].unique()
        disease_to_number = {disease: idx for idx, disease in enumerate(unique_diseases)}
        data['Disease Code'] = data['Finding Label'].map(disease_to_number)
        train_df, test_df = train_test_split(data, test_size=test_split_ratio,train_size=(1-test_split_ratio),random_state=42)
        test_df.reset_index(drop=True, inplace=True)
        print("Test DataFrame created.")
    
    # weights = models.ResNet50_Weights.DEFAULT  # Use the same pretrained weights
    weights = models.ResNet50_Weights.DEFAULT
    model = models.resnet50(weights=weights)
    model.fc = nn.Linear(model.fc.in_features, 15)  # Match the output layer

    # Load the state_dict and fix keys
    state_dict = torch.load(model_path, map_location="cuda:0")
    # Remove the `.module` prefix for models that were compiled using nn.Parellel
    new_state_dict = {key.replace("module.", ""): value for key, value in state_dict.items()}

    # Load the updated state_dict
    model.load_state_dict(new_state_dict)
    model=model.to(device)

    # Set to eval mode
    model.eval()
    # Define transforms
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485], [0.229])
    ])

    # Get test dataset and dataloader
    image_paths = glob.glob(os.path.join(dataset_dir, 'images_*', 'images', '*.png'))
    test_dataset = NIH_dataset(df=test_df, image_directories=image_paths, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    print(len(test_dataset))

    # Initialize metrics
    metrics = Metrics()
    len_test_loader= len(test_loader)


    # Testing loop
    with torch.no_grad():
        for inputs, labels in tqdm.tqdm(test_loader, desc="Testing Batches"):
            inputs = inputs.to(device)
            labels = torch.tensor([disease_to_number[label] for label in labels]).to(device)
            
            outputs = model(inputs)
            _, out_lab = torch.max(outputs, 1)
            loss = criterion(outputs, labels)

            metrics.compute(labels.cpu(), out_lab.cpu(), loss=loss)
        return model,metrics,len_test_loader



model,metrics,group_size = test(
    model_path="resnet50_trained.pth",               
    use_saved_dataframe=False,            
    test_df_path="test_df.pkl",          
    dataset_dir="./dataset",             
    test_split_ratio=0.20,                     
    batch_size=512                                                
)

# metrics.process_by_groups(group_size=1)

print(metrics)
metrics.plot(save=True, path=".", show=True)

