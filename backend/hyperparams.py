# Separator: '-'
params = {
    'MODEL_ARCH': 'EfficientNet',
    'MODEL_NAME': 'efficientnet_b4',
    'PRETRAINED': True,
    'EPOCHS': 100,
    'LR': 0.008,
    'OPTIMIZER': 'SGD',
    'WEIGHT_DECAY': 0.003, # Default = 0
    'MOMENTUM': 0.9, # Default = 0.9 for timm
    'BATCH_SIZE': 512,
    'IMAGE_SIZE': 64,
    'SHOW_PLOTS': False,
    'NUM_WORKERS': 4,
    'NUM_CLASSES': 100,
    'DATA_DIR': "D:\\College\\4ZP6A-capstone\\backend\\dataset"
}