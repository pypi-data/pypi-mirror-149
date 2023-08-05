import logging
import os
from argparse import ArgumentParser

logger = logging.getLogger(__name__)


def get_argparser():
    parser = ArgumentParser(description='Launch a graphic DeepSleep prediction'
                                        ' visualization tool')
    parser.add_argument("--model_dir", type=str, required=False,
                        help="An optional path to a DeepSleep model directory"
                             " from which the GUI will be initialized. "
                             "If not specificed, a model is chosen through the "
                             "GUI.")
    parser.add_argument("--subject_dir", type=str, required=False,
                        help="An optional path to a PSG file to start_predict_thread on. "
                             "If not specificed, a file is chosen through the "
                             "GUI.")
    return parser


def run(model_dir, subject_dir):
    from utime.gui.__main__ import run_gui
    run_gui(model_dir=os.path.abspath(model_dir) if model_dir else None,
            subject_dir=os.path.abspath(subject_dir) if subject_dir else None)


def entry_func(args=None):
    # Get the script to execute, parse only first input
    parser = get_argparser()
    args = vars(parser.parse_args(args))
    run(**args)


if __name__ == "__main__":
    entry_func()
