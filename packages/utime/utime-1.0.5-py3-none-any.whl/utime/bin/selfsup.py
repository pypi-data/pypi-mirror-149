import torch
from torch.utils.data import TensorDataset, DataLoader
from psg_utils.dataset import SleepStudyDataset
from argparse import ArgumentParser
from utime.models.byol_1d import BYOL
from pytorch_lightning.trainer import Trainer


def get_argparser():
    """
    Returns an argument parser for this script
    """
    parser = ArgumentParser(description='Fit a self-supervised model.')
    parser.add_argument('--train_dataset_folder', type=str, required=True)
    parser.add_argument('--val_dataset_folder', type=str, required=True)
    parser.add_argument('--channels', type=str, nargs=2, required=True)
    parser.add_argument('--folder_regex', type=str, default=None)
    parser.add_argument('--psg_regex', type=str, default=None)
    parser.add_argument('--hyp_regex', type=str, default=None)
    return parser


def preprocess(dataset, channels):
    dataset.set_sample_rate(128)
    dataset.set_scaler("RobustScaler")
    dataset.set_strip_func("strip_to_match")
    dataset.set_quality_control_func("clip_noisy_values", min_max_times_global_iqr=20)
    dataset.set_select_channels(channels)
    return dataset


def entry_func(args=None):
    # Get the script to execute, parse only first input
    parser = get_argparser()
    args = parser.parse_args(args)

    # Init train/val datasets
    train = SleepStudyDataset(data_dir=args.train_dataset_folder,
                              folder_regex=args.folder_regex,
                              psg_regex=args.psg_regex,
                              hyp_regex=args.hyp_regex,
                              period_length_sec=30,
                              identifier="TRAIN")
    val = SleepStudyDataset(data_dir=args.val_dataset_folder,
                            folder_regex=args.folder_regex,
                            psg_regex=args.psg_regex,
                            hyp_regex=args.hyp_regex,
                            period_length_sec=30,
                            identifier="VAL")

    # Get preprocessed data as numpy arrays
    X_train, y_train = preprocess(train, args.channels).load().get_all_periods(stack=True)
    X_val, y_val = preprocess(val, args.channels).load().get_all_periods(stack=True)
    assert X_train.shape[-1] == 2 and X_val.shape[-1] == 2

    print(X_train.shape, y_train.shape)
    print(X_val.shape, y_val.shape)

    # Create Torch datasets
    train = TensorDataset(torch.movedim(torch.as_tensor(X_train).float(), 1, 2),
                          torch.as_tensor(y_train).long())
    val = TensorDataset(torch.movedim(torch.as_tensor(X_val).float(), 1, 2),
                        torch.as_tensor(y_val).long())

    # Create dataloaders
    train = DataLoader(train, batch_size=128, shuffle=True)
    val = DataLoader(val, batch_size=128, shuffle=False)

    # Init self-sup model
    model = BYOL(in_channels=1,
                 base_encoder='resnet18',
                 encoder_out_dim=256,
                 projector_hidden_size=128,
                 projector_out_dim=64)

    trainer = Trainer(max_epochs=100, gpus=1)
    trainer.fit(model, train_dataloader=train, val_dataloaders=val)


if __name__ == "__main__":
    entry_func()
