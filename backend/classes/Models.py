import timm
from torch import nn
import torch

class EfficientNet(nn.Module):
    def __init__(self, num_classes: int, version: str, pretrained: bool):
        """
        Initializes the EfficientNet model.

        Args:
            num_classes (int): The number of classes for the output layer.
            version (str): The version of the EfficientNet model to load. This is going to be passed to timm's create_model
            pretrained (bool): Whether to load a pretrained model.
        """
        super(EfficientNet, self).__init__()
        # Load the EfficientNet model
        self.model = timm.create_model(
            version, pretrained=pretrained, num_classes=num_classes
        )

    def forward(self, x):
        """
        Defines the forward pass of the model.

        Args:
            x: The input tensor.

        Returns:
            The output tensor after passing through the model.
        """
        return self.model(x)


class ResNet(nn.Module):
    def __init__(self, num_classes: int, version: str, pretrained: bool):
        """
        Initializes the ResNet model.

        Args:
            num_classes (int): The number of classes for the output layer.
            version (str): The version of the ResNet model to load. This is going to be passed to timm's create_model
            pretrained (bool): Whether to load a pretrained model.
        """
        super(ResNet, self).__init__()
        # Load the ResNet model
        self.model = timm.create_model(
            version, pretrained=pretrained, num_classes=num_classes
        )

    def forward(self, x):
        """
        Defines the forward pass of the model.

        Args:
            x: The input tensor.

        Returns:
            The output tensor after passing through the model.
        """
        return self.model(x)
    
class DenseNet(nn.Module):
    def __init__(self, num_classes: int, version: str, pretrained: bool):
        """
        Initializes the DenseNet model.

        Args:
            num_classes (int): The number of classes for the output layer.
            version (str): The version of the DenseNet model to load. This is going to be passed to timm's create_model
            pretrained (bool): Whether to load a pretrained model.
        """
        super(DenseNet, self).__init__()
        # Load the DenseNet model
        # self.model = timm.create_model(
        #     version, pretrained=pretrained, num_classes=num_classes
        # )

        self.features = timm.create_model(
            version, 
            pretrained=pretrained,
            features_only=True,
            drop_rate=0.2  # Add dropout between dense blocks
        )
        
        # Get feature dimensions from last layer
        last_channel = self.features(torch.randn(1,3,512,512))[-1].shape[1]
        
        # Enhanced classifier head
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(last_channel, 512),
            nn.BatchNorm1d(512),
            nn.SiLU(),  # Swish activation
            nn.Dropout(0.50),  # Main dropout layer
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        """
        Defines the forward pass of the model.

        Args:
            x: The input tensor.

        Returns:
            The output tensor after passing through the model.
        """
        # return self.model(x)
    
        features = self.features(x)[-1]  # Get last feature map
        return self.classifier(features)
