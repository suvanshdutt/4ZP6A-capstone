from argparse import ArgumentParser, Namespace
from backend.CONFIG import params


def parse_arguments(parser: ArgumentParser) -> Namespace:
    """
    Parses command-line arguments using the provided ArgumentParser.

    Args:
        parser (ArgumentParser): The argument parser to which arguments will be added.

    Returns:
        Namespace: An object containing the parsed arguments.
    """

    parser.add_argument(
        "--model_arch",
        type=str,
        default=params["MODEL_ARCH"],
        help="The architecture of the model to use for training.",
    )

    parser.add_argument(
        "--model_name",
        type=str,
        default=params["MODEL_NAME"],
        help="The name of the model to use for training. This is typically what is passed to the timm.create_model function.",
    )

    parser.add_argument(
        "--pretrained",
        type=bool,
        default=params["PRETRAINED"],
        help="Whether to use a pretrained model.",
    )

    parser.add_argument(
        "--batch_size",
        type=int,
        default=params["BATCH_SIZE"],
        help="The batch size for the training.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=params["EPOCHS"],
        help="The number of epochs for training.",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=params["LR"],
        help="The learning rate for the optimizer.",
    )
    parser.add_argument(
        "--optimizer",
        type=str,
        default=params["OPTIMIZER"],
        help="The optimizer to use for training.",
    )
    parser.add_argument(
        "--weight_decay",
        type=float,
        default=params["WEIGHT_DECAY"],
        help="The weight decay for the optimizer.",
    )
    parser.add_argument(
        "--momentum",
        type=float,
        default=params["MOMENTUM"],
        help="The momentum for the optimizer.",
    )
    parser.add_argument(
        "--image_size",
        type=int,
        default=params["IMAGE_SIZE"],
        help="The size of the input images.",
    )
    parser.add_argument(
        "--show_plots",
        type=bool,
        default=params["SHOW_PLOTS"],
        help="Whether to show plots during training.",
    )
    parser.add_argument(
        "--num_workers",
        type=int,
        default=params["NUM_WORKERS"],
        help="The number of worker threads for data loading.",
    )
    parser.add_argument(
        "--num_classes",
        type=int,
        default=params["NUM_CLASSES"],
        help="The number of classes in the dataset.",
    )
    parser.add_argument(
        "--root_dir",
        type=str,
        default=params["ROOT_DIR"],
        help="The root directory for the dataset.",
    )
    parser.add_argument(
        "--train_size",
        type=float,
        default=params["TRAIN_SIZE"],
        help="The size of the training set as a fraction of the total dataset.",
    )
    parser.add_argument(
        "--test_size",
        type=float,
        default=params["TEST_SIZE"],
        help="The size of the validation set as a fraction of the total dataset.",
    )
    return parser.parse_args()
