# Import required hyperparams
import torch
from hyperparams import out_features, disease_to_number

# Importing the necessary libraries
from matplotlib import pyplot as plt
from torchmetrics import MetricCollection
from torchmetrics.wrappers import MetricTracker
from torchmetrics.classification import MulticlassConfusionMatrix, MulticlassPrecision, MulticlassRecall, MulticlassF1Score, MulticlassROC, MulticlassSpecificity, MulticlassAccuracy


# Define the metrics collection. To extend the metrics, add more metrics to the list and if the metric
# is not scalar, add plot code to the metrics_plot function
metrics_collection = MetricCollection([
    MulticlassConfusionMatrix(num_classes=out_features),
    MulticlassPrecision(num_classes=out_features),
    MulticlassRecall(num_classes=out_features),
    MulticlassF1Score(num_classes=out_features),
    MulticlassROC(num_classes=out_features),
    MulticlassSpecificity(num_classes=out_features),
    MulticlassAccuracy(num_classes=out_features),
])


def metrics_plot(train_tracker: MetricTracker, val_tracker: MetricTracker=None, save: bool = False, title1: str = "Train", title2: str = "Validation") -> None:
    """
    This function plots the metrics for the training and validation trackers. The function will plot the confusion matrix, ROC curve and the scalar metrics.
    :param train_tracker: torchmetrics MetricTracker wrapper for the training metrics
    :param val_tracker: Optional torchmetrics MetricTracker wrapper for the validation metrics
    :param save: True if the plot should be saved, False otherwise
    :param title1: Title to use for the first plot. Default is "Train"
    :param title2: Title to use for the second plot. Default is "Validation"
    :return: figure and axes for the plots
    """

    # Helper function to plot the metrics
    def _plot(tracker: MetricTracker, title: str):
        # Get the results
        all_results = tracker.compute_all()

        # Get figures and axes for training plots
        fig = plt.figure(figsize=(40, 20)) # Biiiiig figure fr
        # Create a grid for the plots - 2x2
        grid_spec = fig.add_gridspec(2, 2)
        # Top left
        ax1 = fig.add_subplot(grid_spec[0, 0])
        # Top right
        ax2 = fig.add_subplot(grid_spec[0, 1])
        # Bottom
        ax3 = fig.add_subplot(grid_spec[1, :])

        # Plot the confusion matrix. We only plot the last epoch
        MulticlassConfusionMatrix(num_classes=out_features).plot(val=all_results[-1][f'{title}_MulticlassConfusionMatrix'], ax=ax1, labels=list(disease_to_number.keys()))
        # Plot the ROC curve. We only plot the last epoch
        MulticlassROC(num_classes=out_features).plot(curve=all_results[-1][f'{title}_MulticlassROC'], ax=ax2, labels=list(disease_to_number.keys()))
        # For the remaining we plot the full history, but we need to extract the scalar values from the results
        scalar_results = [
            {k: v for k, v in ar.items() if isinstance(v, torch.Tensor) and v.numel() == 1} for ar in all_results
        ]

        # Set the titles
        ax1.set_title(f'{title} Confusion Matrix')
        ax2.set_title(f'{title} ROC Curve')
        ax3.set_title(f'{title} Metrics')

        # Plot the metrics
        # noinspection PyTypeChecker
        tracker.plot(val=scalar_results, ax=ax3)
        # Save the plot if needed
        if save:
            plt.savefig(f'{title}_metrics.png')


    if val_tracker is not None:
        _plot(val_tracker, title2)
    _plot(train_tracker, title1)






















