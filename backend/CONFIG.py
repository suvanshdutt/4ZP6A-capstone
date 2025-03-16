# Separator: '-'
params = {
    "MODEL_ARCH": "DenseNet",
    "MODEL_NAME": "densenet201",
    "PRETRAINED": True,
    "EPOCHS": 50,
    "LR": 0.0001, # use = 0.0001
    "OPTIMIZER": "AdamW",
    "WEIGHT_DECAY": 0.00001,  # best = 0.00001
    "MOMENTUM": 0.9,  # Default = 0.9 for timm
    "BATCH_SIZE": 16,
    "IMAGE_SIZE": 512,
    "SHOW_PLOTS": False,
    "NUM_WORKERS": 20,
    "NUM_CLASSES": 14,
    "DEVICES": 2,
    "TRAIN_SIZE": 0.75,
    "VAL_SIZE": 0.1,
    "TEST_SIZE": 0.15,
    "ROOT_DIR": "/u20/<MacId>", # replace <MacId> with your mac id
}
