import logging
import os
from argparse import ArgumentParser
from glob import glob

logger = logging.getLogger(__name__)


def get_argparser():
    parser = ArgumentParser(description="Update the 'views' folder to correct "
                                        "home directory paths for the given "
                                        "system,")
    parser.add_argument("--views_folder", type=str, default="./views",
                        help='Path to the folder storing views to be updated.')
    parser.add_argument("--data_dir", type=str, default="./",
                        help="Path to folder storing the actual data.")
    return parser


def update_list_of_files(list_path, new_base_dir, data_dir_name):
    if not os.path.exists(list_path):
        raise OSError(f"Did not find files list at path {list_path}")
    with open(list_path, "r") as in_f:
        data = in_f.readlines()
    corrected = []
    for l in data:
        p = f"{new_base_dir}/{data_dir_name}{l.split(data_dir_name)[-1]}"
        if os.path.exists(p.strip("\n")):
            corrected.append(p)
        else:
            raise OSError("Path {} corrected to {} does not lead to an "
                          "existing file.".format(repr(l.strip("\n")),
                                                  repr(p.strip("\n"))))
    if len(corrected) != len(data):
        raise NotImplementedError("New list of files is length {}, while the "
                                  "original was {}. This is an implementation "
                                  "error!".format(len(corrected), len(data)))
    new_data = "".join(corrected)
    with open(list_path, "w") as out_f:
        out_f.write(new_data)


def update_sub_split(sub_split_dir, new_base_dir, data_dir_name):
    data_splits = glob(sub_split_dir + "/**/LIST_OF_FILES.txt", recursive=True)
    for data in data_splits:
        update_list_of_files(data,  # data + "/LIST_OF_FILES.txt",
                             new_base_dir,
                             data_dir_name)


def update_split(split_dir, new_base_dir, data_dir_name):
    sub_splits = glob(split_dir + "/split*")
    for sub_split in sub_splits:
        update_sub_split(sub_split, new_base_dir, data_dir_name)


def run(views_folder, data_dir):
    splits = glob(os.path.abspath(views_folder) + "/*")
    new_base_dir, data_dir_name = os.path.split(os.path.abspath(data_dir))
    for split in splits:
        logger.info("[*] Updating {}".format(split))
        update_split(split, new_base_dir, data_dir_name)


def entry_func(args=None):
    # Get the script to execute, parse only first input
    parser = get_argparser()
    args = vars(parser.parse_args(args))
    run(**args)


if __name__ == "__main__":
    entry_func()
