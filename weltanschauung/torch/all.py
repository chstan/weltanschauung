## A fairly standard header for working with torch

import os
import random
from pathlib import Path

import torch
from torch import nn, optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split

import pytorch_lightning as pl
import matplotlib.pyplot as plt

from .trainer import Trainer
from .lightning_module import Split, When, LightningModule