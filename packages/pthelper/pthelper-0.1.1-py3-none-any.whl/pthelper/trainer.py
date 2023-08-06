import time
from typing import Union, Tuple, Callable

import numpy as np
import torch

import pthelper.utils as utils


class PTHelper:
    def __init__(
        self,
        model: object,
        device: torch.device,
        criterion: object,
        optimizer: torch.optim.Optimizer,
    ):
        """Trainer class containing the boilerplate code for training and evaluation.

        Args:
        -----
            model (object): PyTorch model object.
            device (torch.device): Device to run training/evaluation on.
            criterion (object): Instance of the loss function being used.
            optimizer (torch.optim.Optimizer): Optimizer used during training.
        """
        self.model = model
        self.device = device
        self.criterion = criterion
        self.optimizer = optimizer

    def train(
        self,
        data_loader: torch.utils.data.DataLoader,
        epoch: int,
        scheduler: Union[Callable, None] = None,
        print_every: int = 100,
    ) -> float:
        """Start training the model.

        Args:
        -----
            data_loader (torch.utils.data.DataLoader): Train dataloader.
            epoch (int): Training epoch.
            scheduler (Union[Callable, None], optional): Learning rate scheduler. Defaults to None.
            print_every (int, optional): Print training stats to console after `print_every` iterations. Defaults to 100.
        """
        batch_time = utils.MetricMonitor()
        data_time = utils.MetricMonitor()
        losses = utils.MetricMonitor()

        # put the model to train mode
        self.model.train()

        start = end = time.time()

        for batch_idx, (images, labels) in enumerate(data_loader):
            # data loading time
            data_time.update(time.time() - end)

            # zero out all the accumulated gradients
            self.optimizer.zero_grad()

            # send the images to the device
            images = images.to(self.device)
            labels = labels.to(self.device)

            batch_size = images.size(0)

            # forward pass
            y_preds = self.model(images)

            # loss value
            loss = self.criterion(y_preds.view(-1), labels.type_as(y_preds))

            # record loss
            losses.update(loss.item(), batch_size)

            # backpropagate
            loss.backward()

            # optimizer update
            self.optimizer.step()

            # elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            # step the scheduler
            if scheduler is not None:
                scheduler.step()

            # diplay results
            if (batch_idx + 1) % print_every == 0:
                print(
                    f"Epoch: [{epoch}][{batch_idx +1} / {len(data_loader)}] "
                    f"Batch time: {batch_time.val:.3f} (avg. {batch_time.avg:.3f}) "
                    f"Elapsed: {utils.time_since(start, float(batch_idx +1) / len(data_loader))} "
                    f"Loss: {losses.val:.4f} (avg. {losses.avg:.4f})"
                )

        return losses.avg

    def evaluate(
        self, data_loader: torch.utils.data.DataLoader, print_every: int = 50
    ) -> Tuple[utils.MetricMonitor, np.ndarray, np.ndarray]:
        """Perform inference on the validation/test data.

        Args:
            data_loader (torch.utils.data.DataLoader): Validation dataloader.
            print_every (int, optional): Print stats after `print_every` iterations. Defaults to 50.
        """
        batch_time = utils.MetricMonitor()
        data_time = utils.MetricMonitor()
        losses = utils.MetricMonitor()

        # switch the model to evaluation mode
        self.model.eval()
        preds = []
        valid_labels = []
        start = end = time.time()
        images_cwt = None
        for batch_idx, (images, labels) in enumerate(data_loader):
            # measure data loading time
            data_time.update(time.time() - end)

            # send the data to device
            images = images.to(self.device)
            # labels = labels.to(self.device)

            batch_size = images.size(0)

            # compute loss with no backprop
            with torch.no_grad():
                y_preds = self.model(images)

            y_preds = y_preds.view(-1)
            loss = self.criterion(y_preds, labels.type_as(y_preds))

            # update the losses
            losses.update(loss.item(), batch_size)

            # record accuracy
            preds.append(torch.sigmoid(y_preds).cpu().numpy())
            valid_labels.append(labels.cpu().numpy())

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            # display results
            if (batch_idx + 1) % print_every == 0:
                print(
                    f"Evaluating: [{batch_idx +1} / {len(data_loader)}] "
                    f"Batch time: {batch_time.val:.3f} (avg. {batch_time.avg:.3f}) "
                    f"Elapsed: {utils.time_since(start, float(batch_idx +1) / len(data_loader))} "
                    f"Loss: {losses.val:.4f} (avg. {losses.avg:.4f})"
                )
        predictions = np.concatenate(preds)
        targets = np.concatenate(valid_labels)

        return losses.avg, predictions, targets
