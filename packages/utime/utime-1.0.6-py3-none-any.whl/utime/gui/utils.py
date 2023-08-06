import os
from utime import Defaults
from utime.hyperparameters import YAMLHParams


def get_attrs_from_model_dir(model_dir):
    params = os.path.join(os.path.abspath(model_dir), "hparams.yaml")
    hparams = YAMLHParams(params, no_version_control=True)

    anot = hparams.get('sleep_stage_annotations')
    if anot:
        classes = {v: defaults.class_int_to_stage_string[v] for v in anot.values()}
        if hparams.get("strip_func") and \
                hparams['strip_func']['strip_func'] == "drop_class":
            del classes[hparams["strip_func"]["class_int"]]
    else:
        classes = {}

    err = "NOT FOUND"
    return {
        "model_name": hparams["build"].get("model_class_name", err),
        "weights": os.path.split(get_best_model(model_dir + "/model"))[-1],
        "classes": classes,
        "Input window (T)": hparams["build"]["batch_shape"][1],
        "Input shape": hparams["build"].get("batch_shape"),
        "Loss func": hparams["fit"]["loss"][0].replace("'", "").replace('"', "")
    }, hparams
