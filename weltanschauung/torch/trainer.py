import socket
from pathlib import Path

import pytorch_lightning as pl
import warnings
from weltanschauung.utils import read_template


class TensorboardInfo:
    @staticmethod
    def is_tensorboard_running() -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("localhost", 6006))
        sock.close()

        return result == 1


def html_repr_logger(logger: pl.loggers.LightningLoggerBase):
    template = read_template(Path("html/logger.html"))
    return template.render(
        logger=logger,
        table_data={
            ".root_dir": logger.root_dir,
            ".log_dir": logger.log_dir,
        },
    )


class Trainer(pl.trainer.Trainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # just setup and get out of the way
        Path(self.logger.log_dir).mkdir(parents=True, exist_ok=True)

        # try to see if tensorboard is available and if not provide instructions
        if not TensorboardInfo.is_tensorboard_running():
            tensorboard_command = f"tensorboard --logdir {self.logger.log_dir}"
            pl._logger.info(
                f"Looked for tensorboard at 127.0.0.1:6006. \nYou should start tensorboard with\n {tensorboard_command}"
            )

    def _repr_html_(self):
        template = read_template(Path("html/trainer.html"))
        return template.render(
            table_data={
                ".current_epoch": self.current_epoch,
                ".deterministic": self.deterministic,
                ".gpus": self.gpus,
                ".max_steps": self.max_steps,
                ".num_gpus": self.num_gpus,
                ".precision": self.precision,
            },
            callback_metrics=self.callback_metrics,
            logger=html_repr_logger(self.logger),
        )
