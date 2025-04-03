from argparse import Namespace
from backend.classes.Classifier import Classifier
from backend.classes.Models import EfficientNet, ResNet, DenseNet


def get_model(args: Namespace) -> Classifier:
    if args.model_arch.lower() == "efficientnet":
        model = EfficientNet(args.num_classes, args.model_name, args.pretrained)
        return Classifier(model, args)
    elif args.model_arch.lower() == "resnet":
        model = ResNet(args.num_classes, args.model_name, args.pretrained)
        return Classifier(model, args)
    elif args.model_arch.lower() == "densenet":
        model = DenseNet(args.num_classes, args.model_name, args.pretrained)
        return Classifier(model, args)
    else:
        raise ValueError(
            "Invalid model architecture. Please choose either EfficientNet, ResNet or DenseNet."
        )
