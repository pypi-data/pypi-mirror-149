from .callbacks_base import TensorboardCallbackBase


class TFTTensorboardCallback(TensorboardCallbackBase):
    def __init__(self, tensorboard_logger):
        super().__init__(tensorboard_logger)

    def update_metrics_scalar(self, trainer, pl_module, phase):
        epoch = pl_module.current_epoch
        if phase == "Train":
            self.tensorboard_logger.experiment.add_scalar(
                f"loss/{phase}", trainer.callback_metrics["train_loss"], epoch
            )
        elif phase == "Validation":
            self.tensorboard_logger.experiment.add_scalar(
                f"loss/{phase}", trainer.callback_metrics["val_loss"], epoch
            )
