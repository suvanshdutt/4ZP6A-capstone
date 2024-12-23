# Separator: '-'
params = {
    "MODEL_ARCH": "EfficientNet",
    "MODEL_NAME": "efficientnet_b4",
    "PRETRAINED": True,
    "EPOCHS": 100,
    "LR": 0.004,
    "OPTIMIZER": "SGD",
    "WEIGHT_DECAY": 0.003,  # Default = 0
    "MOMENTUM": 0.9,  # Default = 0.9 for timm
    "BATCH_SIZE": 90,
    "IMAGE_SIZE": 320,
    "SHOW_PLOTS": False,
    "NUM_WORKERS": 30,
    "NUM_CLASSES": 15,
    "TRAIN_SIZE": 0.8,
    "VAL_SIZE": 0.2,
    "ROOT_DIR": "D:\\College\\4ZP6A-capstone\\backend",
}
