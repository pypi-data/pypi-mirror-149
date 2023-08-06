# Overview
This library contains tools for evaluating fidelity and privacy of synthetic data.

## Usage

Import the desired modules from the library:

```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tonic_reporting import univariate, multivariate, privacy
```

**Preface**

*Numeric* columns refer to columns *encoded* as numeric. Numerical data types in the schema underlying a model may be encoded as other types.

*Categorical* columns refer to columns *encoded* as categorical.

*source_df* is a Pandas DataFrame of original data from the source database

*synth_df* is a Pandas DataFrame of sampled data from trained models

The source and synthetic DataFrames should be equal in row count and schema.

**Numeric Column Statistics**

`univariate.summarize_numeric(source_df, synth_df, numeric_cols)`

**Categorical Column Statistics**

`univariate.summarize_categorical(source_df, synth_df, categorical_cols)`

**Numeric Column Comparative Histograms**

```
fig, axarr = plt.subplots(1, len(numeric_cols), figsize = (9,12))
axarr = axarr.ravel()

for col, ax in zip(numeric_cols, axarr):
    univariate.plot_histogram(source_df, synth_df, col,ax)
```

**Categorical Column Comparative Frequency Tables**

```
for col in categorical_cols:
    univariate.plot_frequency_table(source_df, synth_df, col, ax)
```

**Numeric Column Aggregates Over Time**

If the data represents time series, we can visualize means and confidence intervals of numeric features
over time:

```
for col in numeric_cols:
    fig, ax = plt.subplots(figsize=(10, 8))
    univariate.plot_events_means(source_df, synth_df, col, order_col, ax=ax)
```

and

```
for col in numeric_cols:
    fig, ax = plt.subplots(figsize=(12, 10))
    univariate.plot_events_confidence_intervals(source_df, synth_df, col, order_col, ax=ax)
```
where `order_col` denotes the time/order column.

**Numeric Column Multivariate Correlations Table**

`multivariate.summarize_correlations(source_df, synth_df, numeric_cols)`

**Numeric Column Multivariate Correlations Heat Map**

```
fig, axarr = plt.subplots(1, 2, figsize=(13, 8))
multivariate.plot_correlations(source_df, synth_df, numeric_cols, axarr=axarr, )
fig.tight_layout()
```

**Distance to Closest Record Comparison**

```
syn_dcr, real_dcr = privacy.compute_dcr(source_df, synth_df, numeric_cols, categorical_cols)

fig, ax = plt.subplots(1,1,figsize=(8,6))
ax.hist(real_dcr,bins=300,label = 'Real vs. real', color='mediumpurple');
ax.hist(syn_dcr,bins=300,label='Synthetic vs. real', color='mediumturquoise');
ax.tick_params(axis='both', which='major', labelsize=14)
ax.set_title('Distances to closest record',fontsize=22)
ax.legend(fontsize=16);
```
