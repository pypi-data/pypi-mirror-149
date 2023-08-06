import pytorch_lightning as pl
import torch
from torch import nn
from torch.nn import functional as F
from torch.optim import Adam
from utime.models import resnets_1d

from copy import deepcopy
from typing import Any, Union

from pl_bolts.callbacks.byol_updates import BYOLMAWeightUpdate
from pl_bolts.models.self_supervised.byol.models import SiameseArm
from pl_bolts.optimizers.lr_scheduler import LinearWarmupCosineAnnealingLR


class MLP(nn.Module):

    def __init__(self, input_dim=2048, hidden_size=4096, output_dim=256):
        super().__init__()
        self.output_dim = output_dim
        self.input_dim = input_dim
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_size, bias=False),
            nn.BatchNorm1d(hidden_size),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_size, output_dim, bias=True),
        )

    def forward(self, x):
        x = self.model(x)
        return x


class SiameseArm(nn.Module):

    def __init__(self,
                 in_channels,
                 encoder='resnet50',
                 encoder_out_dim=2048,
                 projector_hidden_size=4096,
                 projector_out_dim=256):
        super().__init__()

        if isinstance(encoder, str):
            encoder = resnets_1d.__dict__[encoder](pretrained=False,
                                                   in_channels=in_channels,
                                                   num_classes=encoder_out_dim)
        # Encoder
        self.encoder = encoder
        # Projector
        self.projector = MLP(encoder_out_dim, projector_hidden_size, projector_out_dim)
        # Predictor
        self.predictor = MLP(projector_out_dim, projector_hidden_size, projector_out_dim)

    def forward(self, x):
        y = self.encoder(x)[0]
        z = self.projector(y)
        h = self.predictor(z)
        return y, z, h


class BYOL(pl.LightningModule):
    """
    PyTorch Lightning implementation of `Bootstrap Your Own Latent (BYOL)
    <https://arxiv.org/pdf/2006.07733.pdf>`_

    Paper authors: Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec, Pierre H. Richemond, \
    Elena Buchatskaya, Carl Doersch, Bernardo Avila Pires, Zhaohan Daniel Guo, Mohammad Gheshlaghi Azar, \
    Bilal Piot, Koray Kavukcuoglu, Rémi Munos, Michal Valko.

    Model implemented by:
        - `Annika Brundyn <https://github.com/annikabrundyn>`_

    Modified for 1D signals by:
        - 'Mathias Perslev <https://github.com/perslev>'_
    """

    def __init__(
            self,
            in_channels,
            warmup_epochs: int = 10,
            max_epochs: int = 1000,
            learning_rate: float = 0.2,
            weight_decay: float = 1.5e-6,
            base_encoder: Union[str, torch.nn.Module] = 'resnet50',
            encoder_out_dim: int = 2048,
            projector_hidden_size: int = 4096,
            projector_out_dim: int = 256
    ):
        """
        Args:
            base_encoder: the base encoder module or resnet name
            encoder_out_dim: output dimension of base_encoder
            projector_hidden_size: hidden layer size of projector MLP
            projector_out_dim: output size of projector MLP
        """
        super().__init__()
        self.save_hyperparameters(ignore='base_encoder')

        self.online_network = SiameseArm(in_channels, base_encoder, encoder_out_dim, projector_hidden_size, projector_out_dim)
        self.target_network = deepcopy(self.online_network)
        self.weight_callback = BYOLMAWeightUpdate()

    def on_train_batch_end(self, outputs, batch: Any, batch_idx: int, dataloader_idx: int) -> None:
        # Add callback for user automatically since it's key to BYOL weight update
        self.weight_callback.on_train_batch_end(self.trainer, self, outputs, batch, batch_idx, dataloader_idx)

    def forward(self, x):
        y, _, _ = self.online_network(x)
        return y

    def shared_step(self, batch, batch_idx):
        signals, y = batch
        chan_1, chan_2 = signals[:, 0:1, :], signals[:, 1:2, :]

        # Image 1 to image 2 loss
        y1, z1, h1 = self.online_network(chan_1)
        with torch.no_grad():
            y2, z2, h2 = self.target_network(chan_2)

        loss_a = -2 * F.cosine_similarity(h1, z2).mean()

        # Image 2 to image 1 loss
        y1, z1, h1 = self.online_network(chan_2)
        with torch.no_grad():
            y2, z2, h2 = self.target_network(chan_1)
        # L2 normalize
        loss_b = -2 * F.cosine_similarity(h1, z2).mean()

        # Final loss
        total_loss = loss_a + loss_b

        return loss_a, loss_b, total_loss

    def training_step(self, batch, batch_idx):
        loss_a, loss_b, total_loss = self.shared_step(batch, batch_idx)

        # log results
        self.log_dict({'1_2_loss': loss_a, '2_1_loss': loss_b, 'train_loss': total_loss})

        return total_loss

    def validation_step(self, batch, batch_idx):
        loss_a, loss_b, total_loss = self.shared_step(batch, batch_idx)

        # log results
        self.log_dict({'1_2_loss': loss_a, '2_1_loss': loss_b, 'val_loss': total_loss})

        return total_loss

    def configure_optimizers(self):
        optimizer = Adam(self.parameters(), lr=self.hparams.learning_rate, weight_decay=self.hparams.weight_decay)
        scheduler = LinearWarmupCosineAnnealingLR(
            optimizer, warmup_epochs=self.hparams.warmup_epochs, max_epochs=self.hparams.max_epochs
        )
        return [optimizer], [scheduler]
