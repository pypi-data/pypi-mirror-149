import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tonic_reporting.util import filter_null_and_match_row_counts
from scipy.stats import pearsonr, spearmanr, kendalltau
from typing import Tuple, List

from tonic_reporting.styling import PlotsSizes


def summarize_correlations(
    real_data: pd.DataFrame,
    synth_data: pd.DataFrame,
    numeric_columns: List[str],
    corr_type="spearman",
) -> pd.DataFrame:
    real_data, synth_data = filter_null_and_match_row_counts(
        real_data, synth_data, numeric_columns
    )

    N = len(numeric_columns)
    corr_data = []
    if corr_type == "pearson":
        corr_fn = pearsonr
    elif corr_type == "spearman":
        corr_fn = spearmanr
    elif corr_type == "kendall":
        corr_fn = kendalltau
    else:
        raise ValueError("corr_type not recognized")

    for i in range(N):
        for j in range(i):
            x_name = numeric_columns[i]
            y_name = numeric_columns[j]
            real_stat, _ = corr_fn(real_data[x_name], real_data[y_name])
            synth_stat, _ = corr_fn(synth_data[x_name], synth_data[y_name])
            row = {
                "Column 1": x_name,
                "Column 2": y_name,
                "Real Correlation": real_stat,
                "Synthetic Correlation": synth_stat,
            }
            corr_data.append(row)

    return pd.DataFrame(corr_data)


def plot_correlations(
    real_data: pd.DataFrame,
    synth_data: pd.DataFrame,
    columns: List[str],
    axarr=None,
    corr_type="spearman",
    title_fontsize=18,
    label_fontsize=10,
):
    real_data, synth_data = filter_null_and_match_row_counts(
        real_data, synth_data, columns
    )

    real_corr = real_data[columns].corr(method=corr_type)
    synth_corr = synth_data[columns].corr()
    if axarr is None:
        fig, axarr = plt.subplots(1, 2, figsize=PlotsSizes.XTRA_LARGE_FIGURE)

    im0 = axarr[0].imshow(real_corr, cmap="Purples")
    axarr[0].set_xticks(np.arange(len(columns)))
    axarr[0].set_yticks(np.arange(len(columns)))
    axarr[0].set_xticklabels(columns, rotation="vertical")
    axarr[0].set_yticklabels(columns)
    axarr[0].set_title("Real Data Correlations", fontsize=title_fontsize)

    im1 = axarr[1].imshow(synth_corr, cmap="Purples")
    axarr[1].set_xticks(np.arange(len(columns)))
    axarr[1].set_yticks(np.arange(len(columns)))
    axarr[1].set_xticklabels(columns, rotation="vertical")
    axarr[1].set_yticklabels(columns)
    axarr[1].set_title("Synthetic Data Correlations", fontsize=title_fontsize)

    axarr[0].tick_params(axis="both", which="major", labelsize=label_fontsize)
    axarr[1].tick_params(axis="both", which="major", labelsize=label_fontsize)
    plt.colorbar(im0, fraction=0.046, pad=0.04, ax=axarr[0])
    plt.colorbar(im1, fraction=0.046, pad=0.04, ax=axarr[1])
