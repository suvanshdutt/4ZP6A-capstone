from argparse import Namespace
from backend.classes.Classifier import Classifier
from backend.classes.Models import EfficientNet, ResNet


def get_model(args: Namespace) -> Classifier:
    match args.model_arch.lower():
        case "efficientnet":
            model = EfficientNet(args.num_classes, args.model_name, args.pretrained)
            return Classifier(model, args)
        case "resnet":
            model = ResNet(args.num_classes, args.model_name, args.pretrained)
            return Classifier(model, args)
        case _:
            raise ValueError(
                "Invalid model architecture. Please choose either EfficientNet or ResNet."
            )
