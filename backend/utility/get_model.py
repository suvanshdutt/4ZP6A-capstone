from argparse import Namespace
from backend.classes.Classifier import Classifier
from backend.classes.Models import EfficientNet, ResNet, DenseNet


def get_model(args: Namespace) -> Classifier:
    match args.model_arch.lower():
        case "efficientnet":
            model = EfficientNet(args.num_classes, args.model_name, args.pretrained)
            return Classifier(model, args)
        case "resnet":
            model = ResNet(args.num_classes, args.model_name, args.pretrained)
            return Classifier(model, args)
        case "densenet":
            model = DenseNet(args.num_classes, args.model_name, args.pretrained)
            return Classifier(model, args)
        case _:
            raise ValueError(
                "Invalid model architecture. Please choose either EfficientNet, ResNet or DenseNet."
            )
