from pathlib import Path
from typing import Optional
import platform
import pytorch_lightning as pl
import torchvision as tv
from torch.utils.data import DataLoader, random_split

from weltanschauung.utils import read_template


__all__ = ["FashionMNISTDataModule", "DEFAULT_DATA_DIRECTORY"]

DEFAULT_DATA_DIRECTORY = Path("E:/datasets/")


class LightningDataModule(pl.LightningDataModule):
    name = None

    def _repr_html_(self):
        template = read_template(Path("html/data_module.html"))
        return template.render(
            dm=self,
            table_data={
                ".dims": self.dims,
                ".batch_size": self.batch_size,
                ".val_split_frac": self.val_split_frac,
                ".data_dir": self.data_dir,
                ".num_workers": self.num_workers,
                ".normalize": self.normalize,
                ".seed": self.seed,
            },
        )


class FashionMNISTDataModule(LightningDataModule):
    name = "fashion-mnist"

    def __init__(
        self,
        data_dir: Optional[str] = None,
        val_split_frac: float = 0.3,
        num_workers: int = 16,
        normalize: bool = False,
        seed: int = 42,
        batch_size: int = 32,
        *args,
        **kwargs
    ):
        super(*args).__init__(**kwargs)

        if data_dir is None:
            data_dir = DEFAULT_DATA_DIRECTORY

        data_dir = Path(data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir = str(data_dir.resolve())

        self.dims = (1, 28, 28)
        self.normalize = normalize
        self.dataset_train = None
        self.dataset_valid = None
        self.test_transforms = self.default_transforms
        self.val_split_frac = val_split_frac
        self.seed = seed
        self.batch_size = batch_size

        if platform.system() == "Windows":
            num_workers = 0

        self.num_workers = num_workers

    def prepare_data(self):
        """
        Download the data to the requested location
        """
        tv.datasets.FashionMNIST(self.data_dir, train=True, download=True)
        tv.datasets.FashionMNIST(self.data_dir, train=False, download=True)

    @property
    def num_classes(self):
        return 10

    def setup(self, stage: Optional[str] = None):
        dset_kwargs = (
            dict(transform=self.default_transforms) if self.default_transforms else {}
        )
        dset = tv.datasets.FashionMNIST(
            self.data_dir, train=True, download=False, **dset_kwargs
        )
        train_length = len(dset)

        n_valid = int(train_length * self.val_split_frac)
        self.dataset_train, self.dataset_valid = random_split(
            dset, [train_length - n_valid, n_valid]
        )

    def train_dataloader(self):
        return DataLoader(
            self.dataset_train,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
            drop_last=True,
            pin_memory=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self.dataset_valid,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            drop_last=True,
            pin_memory=True,
        )

    def test_dataloader(self):
        dset_kwargs = (
            dict(transform=self.test_transforms) if self.test_transforms else {}
        )
        dset = tv.datasets.FashionMNIST(
            self.data_dir, train=False, download=False, **dset_kwargs
        )
        return DataLoader(
            dset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            drop_last=True,
            pin_memory=True,
        )

    @property
    def default_transforms(self):
        if self.normalize:
            transforms = [
                tv.transforms.ToTensor(),
                tv.transforms.Normalize(mean=(0.5,), std=(0.5,)),
            ]
        else:
            transforms = [
                tv.transforms.ToTensor(),
            ]

        return tv.transforms.Compose(transforms)
