# Separator: '-'
params = {
    "MODEL_ARCH": "DenseNet",
    "MODEL_NAME": "densenet121",
    "PRETRAINED": True,
    "EPOCHS": 3,
    "LR": 0.0001,
    "OPTIMIZER": "Adam",
    "WEIGHT_DECAY": 0.0,  # Default = 0
    "MOMENTUM": 0.9,  # Default = 0.9 for timm
    "BATCH_SIZE": 64,
    "IMAGE_SIZE": 320,
    "SHOW_PLOTS": False,
    "NUM_WORKERS": 20,
    "NUM_CLASSES": 14,
    "TRAIN_SIZE": 0.9,
    "TEST_SIZE": 0.1,
    "ROOT_DIR": "F:",
}
