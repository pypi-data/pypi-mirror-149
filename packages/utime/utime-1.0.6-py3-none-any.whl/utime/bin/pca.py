import logging
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from sklearn.decomposition import PCA
from sklearn.manifold import Isomap, MDS, TSNE, LocallyLinearEmbedding
from mpl_toolkits.mplot3d import Axes3D
from utime import Defaults

logger = logging.getLogger(__name__)


def get_argparser():
    parser = ArgumentParser(description='Visualize the prediction confidence '
                                        'in a 2D plot.')
    parser.add_argument('-f', type=str, required=True,
                        help="Input file. Must be a .npy file of shape (Nx5)")
    parser.add_argument('-l', type=str, required=False,
                        help="Optional label giving the true label for all N "
                             "data points in the file specified by -f. "
                             "Must be a .npy file of shape (Nx1)")
    parser.add_argument("--3D", action="store_true")
    parser.add_argument("--sample", type=int, default=None,
                        help="Number of points to sample for plotting. "
                             "Defaults to 100K for 2D and 10K for 3D.")
    return parser


def _plot_with_true_colors(ax, true, pred):
    for cls_idx in np.unique(true):
        idx = np.where(true == cls_idx)
        ax.scatter(*pred[idx].T,
                   label=Defaults.get_class_int_to_stage_string()[cls_idx])
        ax.legend(loc=0, fontsize=16)


def entry_func(args=None):
    # Get the script to execute, parse only first input
    parser = get_argparser()
    args = vars(parser.parse_args(args))

    pred = np.load(args['f'])
    if args['l']:
        true = np.load(args['l'])
    else:
        true = None

    sample = args["sample"] or (10**4 if args["3D"] else 10**5)
    to_plot = np.random.choice(np.arange(len(pred)), sample, replace=False)
    pred = pred[to_plot]
    if true is not None:
        true = true[to_plot]

    # Run PCA to 2 componenets
    logger.info("Running TSNE")
    pca = PCA(n_components=3 if args["3D"] else 2)
    pred = pca.fit_transform(pred)
    logger.info("DONE")

    # Make figure
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection="3d" if args["3D"] else None)

    if true is not None:
        _plot_with_true_colors(ax, true, pred)
    else:
        ax.scatter(*pred.T)

    plt.show()


if __name__ == "__main__":
    entry_func()

