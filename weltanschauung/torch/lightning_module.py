import enum
import pytorch_lightning as pl

__all__ = ["Split", "When", "LightningModule"]


class Split(str, enum.Enum):
    TRAIN = "train"
    VALID = "valid"
    TEST = "test"


class When(str, enum.Enum):
    STEP = "step"
    EPOCH = "epoch"


class LightningModule(pl.LightningModule):
    def log_metrics(self, split, on_step=None, on_epoch=True, **metrics):
        inner_key = split.value

        if on_step is None:
            on_step = split == Split.TRAIN

        logs = {
            f"{name}": {
                inner_key: value.item(),
            }
            for name, value in metrics.items()
        }
        self.log_dict(logs, on_step=on_step, on_epoch=on_epoch)