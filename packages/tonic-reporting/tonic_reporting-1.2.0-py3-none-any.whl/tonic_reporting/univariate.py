from typing import Tuple, List, Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tonic_reporting.util import filter_null_and_match_row_counts
from scipy.stats import ks_2samp, anderson_ksamp, chisquare
from scipy.special import kl_div


def summarize_numeric(
    real_data: pd.DataFrame, synth_data: pd.DataFrame, columns: List[str]
) -> pd.DataFrame:
    rows = []
    for col in columns:
        real = real_data[col]
        fake = synth_data[col]
        anderson_stat, _, anderson_p_val = anderson_ksamp([real, fake])
        ks_stat, ks_p_val = ks_2samp(real, fake)
        row = {
            "Column": col,
            "Anderson-Darling statistic": anderson_stat,
            "Anderson-Darling p-value": anderson_p_val,
            "Kolmogorov-Smirnov statistic": ks_stat,
            "Kolmogorov-Smirnov p-value": ks_p_val,
        }

        rows.append(row)
    return pd.DataFrame(rows)


def get_frequencies(
    real_series: pd.Series, synthetic_series: pd.Series
) -> Tuple[np.ndarray, np.ndarray]:
    """Gets frequencies for each value in real and synthetic series. Assumes synthetic series values
    are subset of series_values
    """
    real_ft = real_series.value_counts()
    fake_ft = synthetic_series.value_counts()
    real_counts = []
    fake_counts = []
    for value in real_ft.keys():
        real_counts.append(real_ft[value])
        fake_counts.append(fake_ft.get(value, 0))
    return np.array(real_counts), np.array(fake_counts)


def chi_square_test(
    real_data: pd.Series, synthetic_data: pd.Series
) -> Tuple[float, float]:
    real_counts, fake_counts = get_frequencies(
        real_data,
        synthetic_data,
    )
    return chisquare(fake_counts, real_counts)


def kl_divergence(real_data: pd.Series, synthetic_data: pd.Series) -> float:
    """Computes D_KL(synthetic_data || real_data)"""
    real_counts, fake_counts = get_frequencies(
        real_data,
        synthetic_data,
    )
    idx = np.where(fake_counts != 0)[0]
    real_probs = real_counts[idx] / sum(real_counts[idx])
    fake_probs = fake_counts[idx] / sum(fake_counts[idx])

    return np.sum(fake_probs * np.log(fake_probs / real_probs))


def summarize_categorical(
    real_data: pd.DataFrame, synth_data: pd.DataFrame, columns: List[str]
) -> pd.DataFrame:
    rows = []
    for col in columns:
        real = real_data[col]
        fake = synth_data[col]

        cs_stat, cs_p_val = chi_square_test(real, fake)
        kl = kl_divergence(real_data[col], synth_data[col])
        row = {
            "Column": col,
            "Chi-Square statistic": cs_stat,
            "Chi-Square p-value": cs_p_val,
            "D_KL(Synth || Real)": kl,
        }
        rows.append(row)
    return pd.DataFrame(rows)


def plot_histogram(
    real_data: pd.DataFrame,
    synth_data: pd.DataFrame,
    col: str,
    ax=None,
    side_by_side=False,
    lower_quantile_lim=0.05,
    upper_quantile_lim=0.95,
):
    real_data, synth_data = filter_null_and_match_row_counts(real_data, synth_data, [col])

    if ax is None:
        fig, ax = plt.subplots(1, 1)
    bins = np.histogram_bin_edges(np.array(real_data[col]), bins="auto")
    if side_by_side:
        ax.hist(
            [real_data[col], synth_data[col]],
            bins=bins,
            color=["mediumpurple", "mediumturquoise"],
            label=["Real", "Synthetic"],
        )
    else:
        ax.hist(
            real_data[col], bins=bins, color="mediumpurple", alpha=0.5, label="Real"
        )
        ax.hist(
            synth_data[col],
            bins=bins,
            color="mediumturquoise",
            alpha=0.5,
            label="Synthetic",
        )
    ax.set_xlim(
        real_data[col].quantile(lower_quantile_lim),
        real_data[col].quantile(upper_quantile_lim),
    )
    ax.legend(fontsize=10)
    ax.set_title(col, fontsize=12)
    ax.tick_params(axis="both", which="major", labelsize=10)
