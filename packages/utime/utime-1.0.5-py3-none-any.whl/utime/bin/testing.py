from argparse import ArgumentParser
from utime import Defaults
import os


def get_argparser():
    parser = ArgumentParser(description='Fit a MultiPlanarUNet model defined in a project folder. '
                                        'Invoke "init_project" to start a new project.')
    parser.add_argument("--no_val", action="store_true")
    return parser


def run(no_val):

    from psg_utils.dataset import SleepStudyDataset
    from utime.hyperparameters import YAMLHParams
    from utime.utils.scriptutils import assert_project_folder

    # Get a logger
    project_dir = os.path.abspath(Defaults.PROJECT_DIRECTORY)
    assert_project_folder(project_dir)

    # Load hparams
    hparams = YAMLHParams(os.path.join(project_dir, "hparams.yaml"))

    # Get annotations
    ann_dict = hparams.get("sleep_stage_annotations")

    # Prepare data
    if no_val or not hparams.get("val_data"):
        data = ("train_data",)
    else:
        data = ("train_data", "val_data")
    data = [SleepStudyDataset(**hparams[d],
                              annotation_dict=ann_dict) for d in data]

    # Apply transformations, scaler etc.
    from utime.utils.scriptutils import select_sample_strip_scale_quality
    select_sample_strip_scale_quality(*data, hparams=hparams)

    # ONLY 4
    for d in data:
        d.pairs = d.pairs[:4]

    # Load data
    for d in data:
        d.load()

    hparams["fit"]["batch_size"] = 2
    hparams["fit"]["margin"] = 5

    # Create train generator
    # cls_weights = hparams.get("class_weights")
    cls_weights = {0: 0.333, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0}
    train_seq = data[0].get_batch_sequence(random_batches=True,
                                           class_weights=cls_weights,
                                           **hparams["fit"])
    if not no_val:
        # Creat val generator
        random_val_batches = bool(hparams["fit"].get("margin"))
        val_seq = data[1].get_batch_sequence(random_batches=random_val_batches,
                                             **hparams["fit"])
    else:
        val_seq = None

    for i in range(3):
        X, y, w = train_seq[i]
        print(X.shape, y.shape, w.shape)
        print(y.squeeze())
        print(w.squeeze())


def entry_func(args=None):
    # Get the script to execute, parse only first input
    parser = get_argparser()
    args = vars(parser.parse_args(args))
    run(**args)


if __name__ == "__main__":
    entry_func()


from visbrain.gui import Sleep