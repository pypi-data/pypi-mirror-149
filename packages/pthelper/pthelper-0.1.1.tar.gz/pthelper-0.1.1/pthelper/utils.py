import sys
import os
import logging
import time
import math
from pathlib import Path
from traceback import print_tb

import torch
from torchinfo import summary


class MetricMonitor:
    """Calculates and stroes the average value of the metrics/loss."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all the parameters to zero."""
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val: float, n: int = 1):
        """Update the value of the metrics and calculate their average value
        over the entire dataset

        Args:
        -----
            val (float): Computed metric (per batch).
            n (int, optional): Batch size. Defaults to 1.
        """
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


class LogParse:
    def __init__(
        self,
        script_name: str,
        model_name: str,
        log_dir: str = None,
        stream_handler: bool = True,
        log_exceptions: bool = True,
    ):
        """Constructor for the logger to log the progress into a file.

        Args:
        -----
            script_name (str): Name of the script outputting the logs.
            model_name (str): Name of the model.
            log_dir (str, optional): Path to the logs directory. Defaults to None.
            args (argparse.Namespace, optional): Argparse namespace object containing the command line arguments. Defaults to None.
            stream_handler (bool, optional): If true, show the logs in the console. Defaults to True.
            log_exceptions (bool, optional): If true, log the exceptions as well. Defaults to True.
        """
        self.logger = None
        self.script_name = script_name
        self.log_file = (
            os.path.join(log_dir, f"{model_name}.log")
            if log_dir is not None
            else None
        )
        self.stream_handler = stream_handler
        self.log_exceptions = log_exceptions

        if not (stream_handler and self.log_file):
            raise TypeError("Logger must have handler.")

        def __call__(self):
            logger = logging.getLogger(name=self.script_name)
            logger.setLevel(level=logging.INFO)

            if self.log_file is not None:
                log_path = Path(self.log_file)
                # make directory for the log file
                log_path.parent.mkdir(parents=True, exist_ok=True)
                # create handlers
                f_handler = logging.FileHandler(log_path.as_posix(), mode="w")
                # create formatters and add them to handlers
                f_format = logging.Formatter(
                    "%(asctime)s:%(name)s: %(levelname)s:%(message)s"
                )
                f_handler.setFormatter(f_format)
                logger.addHandler(f_handler)

            # display logs in console
            if self.stream_handler:
                s_handler = logging.StreamHandler()
                s_format = logging.Formatter(
                    "%(name)s: %(levelname)s:%(message)s"
                )
                s_handler.setFormatter(s_format)
                logger.addHandler(s_handler)

            self.logger = logger

            if self.log_exceptions:
                sys.excepthook = self._log_exceptions()

            return logger

        def _log_exceptions(self):
            def e_handler(type, value, tb):
                print_tb(tb)
                self.logger.exception(f" {type.__name__}: {value}")

            return e_handler

        @staticmethod
        def get_global_logger():
            logger = logging.getLogger("__main__")
            if not logger.hasHandlers():
                raise AttributeError(
                    "No logger exists. Logger must be declared."
                )
            return logger


def time_since(since: int, percent: float) -> str:
    """Helper function to time the training and evaluation process.

    Args:
    -----
        since (int): Start time.
        percent (float): Percent to the task done.

    Returns:
    --------
        str: Print elapsed/remaining time to console.
    """

    def as_minutes_seconds(s: float) -> str:
        m = math.floor(s / 60)
        s -= m * 60
        m, s = int(m), int(s)
        return f"{m:2d}m {s:2d}s"

    now = time.time()
    elapsed = now - since
    total_estimated = elapsed / percent
    remaining = total_estimated - elapsed
    return f"{as_minutes_seconds(elapsed)} (remain {as_minutes_seconds(remaining)}"


def get_model_params(model: torch.nn.Module) -> int:
    """Helper function to determine the total number of the trainable parameters
    in the PyTorch model.

    Args:
    -----
        model (torch.nn.Module): Instance of the PyTorch model being used.

    Returns:
    --------
        int: Number of the trainable parameters.
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def model_details(
    model: torch.nn.Module,
    x: torch.Tensor,
    input_size: tuple,
    device: torch.device,
):
    """Print Keras like model details on the console.

    Args:
    -----
        model (torch.nn.Module): Instance of the PyTorch model being used.
        x (torch.Tensor): Dummy input.
        input_size (tuple): Size of the input.
    """
    print("\t\t\t\tMODEL SUMMARY")
    summary(model, input_size=input_size, device=device)
    print(f"Batched input size: {x.shape}")
    print(f"Batched output size: {model(x).shape}")
    print(f"Model contains {get_model_params(model)} trainable parameters.")
