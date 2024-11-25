from torch import nn, optim

# Hyperparameters
epochs = 100 # How many iterations through the dataset to train the model
learning_rate = 0.0005 # How much to update the weights of the model
train_batch_size = 64 # How many images to use in one batch
test_batch_size = 128 # How many images to use in one batch
train_size = 0.0001 # How much of the dataset to use for training
validation_size = 0.0001 # How much of the dataset to use for validation
test_size = 0.01 # How much of the dataset to use for testing
out_features = 14 # How many classes to predict

# Set optimizer
optimizer = optim.AdamW # Reference to the optimizer class (not an instance)
# Loss function. All parameters are known, so we can use the class instance directly
criterion = nn.CrossEntropyLoss()

# Disease to number mapping / Label encoding
disease_to_number = {'Cardiomegaly': 0,
                     'Emphysema': 1,
                     'Effusion': 2,
                     'Hernia': 3,
                     'Infiltration': 4,
                     'Mass': 5,
                     'Nodule': 6,
                     'Atelectasis': 7,
                     'Pneumothorax': 8,
                     'Pleural_Thickening': 9,
                     'Pneumonia': 10,
                     'Fibrosis': 11,
                     'Edema': 12,
                     'Consolidation': 13}

