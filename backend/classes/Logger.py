import numpy as np
from argparse import Namespace
from typing import Optional, Union, Dict, Any
from clearml import Task
from lightning.pytorch.loggers import Logger


class ClearMLLogger(Logger):
    """
    A logger class that integrates ClearML with PyTorch Lightning.

    Attributes:
        task (Task): The ClearML task object.
        logger: The logger object from the ClearML task.
        _version (Optional[int]): The version of the logger.
    """

    def __init__(self, task: Task, version: Optional[int] = None):
        """
        Initializes the ClearMLLogger.

        Args:
            task (Task): The ClearML task object.
            version (Optional[int]): The version of the logger. Defaults to None.
        """
        super().__init__()
        self.task = task
        self.logger = self.task.get_logger()
        self._version = version

    @property
    def version(self) -> Optional[Union[int, str]]:
        """
        Returns the version of the logger.

        Returns:
            Optional[Union[int, str]]: The version of the logger.
        """
        return self._version

    @property
    def name(self) -> Optional[str]:
        """
        Returns the name of the ClearML task.

        Returns:
            Optional[str]: The name of the ClearML task.
        """
        return self.task.name

    def log_metrics(
        self, metrics: Dict[str, float], step: Optional[int] = None
    ) -> None:
        """
        Logs metrics to ClearML.

        Args:
            metrics (Dict[str, float]): A dictionary of metric names and values.
            step (Optional[int]): The step or iteration at which the metrics are logged. Defaults to None.
        """
        for key, value in metrics.items():
            # Separate key into title and series if it contains '/'
            title, series = key.split("/") if "/" in key else (key, key)
            if step is not None:
                if series == title:
                    self.logger.report_single_value(name=title, value=value)
                else:
                    self.logger.report_scalar(
                        title=title, series=series, value=value, iteration=step
                    )
            else:
                self.logger.report_single_value(name=title, value=value)

    def report_confusion_matrix(
        self,
        title: str,
        series: str,
        matrix: np.ndarray,
        iteration=None,
        xaxis=None,
        yaxis=None,
        xlabels=None,
        ylabels=None,
        yaxis_reversed=False,
        comment=None,
        extra_layout=None,
    ):
        """
        Reports a confusion matrix to ClearML.

        Args:
            title (str): The title of the confusion matrix.
            series (str): The series name of the confusion matrix.
            matrix (np.ndarray): The confusion matrix data.
            iteration: The iteration at which the confusion matrix is reported. Defaults to None.
            xaxis: The label for the x-axis. Defaults to None.
            yaxis: The label for the y-axis. Defaults to None.
            xlabels: The labels for the x-axis ticks. Defaults to None.
            ylabels: The labels for the y-axis ticks. Defaults to None.
            yaxis_reversed (bool): Whether to reverse the y-axis. Defaults to False.
            comment: Additional comments. Defaults to None.
            extra_layout: Extra layout options. Defaults to None.
        """
        self.logger.report_confusion_matrix(
            title=title,
            series=series,
            matrix=matrix,
            iteration=iteration,
            xaxis=xaxis,
            yaxis=yaxis,
            xlabels=xlabels,
            ylabels=ylabels,
            yaxis_reversed=yaxis_reversed,
            comment=comment,
            extra_layout=extra_layout,
        )

    def log_hyperparams(
        self,
        params: Union[Dict[str, Any], Namespace],
        name: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Logs hyperparameters to ClearML.

        Args:
            params (Union[Dict[str, Any], Namespace]): The hyperparameters to log.
            name (Optional[str]): The name of the hyperparameters set. Defaults to None.
        """
        self.task.connect(params, name=name)
