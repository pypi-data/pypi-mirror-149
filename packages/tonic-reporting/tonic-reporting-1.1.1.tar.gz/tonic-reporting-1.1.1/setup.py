# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tonic_reporting']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0.0,<4.0.0',
 'numpy>=1.0.0,<2.0.0',
 'pandas>=1.0.0,<2.0.0',
 'scikit-learn>=1.0.0,<2.0.0',
 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'tonic-reporting',
    'version': '1.1.1',
    'description': 'Tools for evaluating fidelity and privacy of synthetic data',
    'long_description': "# Overview\nThis library contains tools for evaluating fidelity and privacy of synthetic data.\n\n## Usage\n\nImport the desired modules from the library:\n\n```\nimport pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom tonic_reporting import univariate, multivariate, privacy\n```\n\n**Preface**\n\n*Numeric* columns refer to columns *encoded* as numeric. Numerical data types in the schema underlying a model may be encoded as other types.\n\n*Categorical* columns refer to columns *encoded* as categorical.\n\n*source_df* is a Pandas DataFrame of original data from the source database\n\n*synth_df* is a Pandas DataFrame of sampled data from trained models\n\nThe source and synthetic DataFrames should be equal in row count and schema.\n\n**Numeric Column Statistics**\n\n`univariate.summarize_numeric(source_df, synth_df, numeric_cols)`\n\n**Categorical Column Statistics**\n\n`univariate.summarize_categorical(source_df, synth_df, categorical_cols)`\n\n**Numeric Column Comparative Histograms**\n\n```\nfig, axarr = plt.subplots(1, len(numeric_cols), figsize = (9,12))\naxarr = axarr.ravel()\n\nfor col, ax in zip(numeric_cols, axarr):\n    univariate.plot_histogram(source_df, synth_df, col,ax)\n```\n\n**Categorical Column Comparative Frequency Tables**\n\n```\nfor col in categorical_cols:\n    univariate.plot_frequency_table(source_df, synth_df, col, ax)\n```\n\n**Numeric Column Aggregates Over Time**\n\nIf the data represents time series, we can visualize means and confidence intervals of numeric features\nover time:\n\n```\nfor col in numeric_cols:\n    fig, ax = plt.subplots(figsize=(10, 8))\n    univariate.plot_events_means(source_df, synth_df, col, order_col, ax=ax)\n```\n\nand\n\n```\nfor col in numeric_cols:\n    fig, ax = plt.subplots(figsize=(12, 10))\n    univariate.plot_events_confidence_intervals(source_df, synth_df, col, order_col, ax=ax)\n```\nwhere `order_col` denotes the time/order column.\n\n**Numeric Column Multivariate Correlations Table**\n\n`multivariate.summarize_correlations(source_df, synth_df, numeric_cols)`\n\n**Numeric Column Multivariate Correlations Heat Map**\n\n```\nfig, axarr = plt.subplots(1, 2, figsize=(13, 8))\nmultivariate.plot_correlations(source_df, synth_df, numeric_cols, axarr=axarr, )\nfig.tight_layout()\n```\n\n**Distance to Closest Record Comparison**\n\n```\nsyn_dcr, real_dcr = privacy.compute_dcr(source_df, synth_df, numeric_cols, categorical_cols)\n\nfig, ax = plt.subplots(1,1,figsize=(8,6))\nax.hist(real_dcr,bins=300,label = 'Real vs. real', color='mediumpurple');\nax.hist(syn_dcr,bins=300,label='Synthetic vs. real', color='mediumturquoise');\nax.tick_params(axis='both', which='major', labelsize=14)\nax.set_title('Distances to closest record',fontsize=22)\nax.legend(fontsize=16);\n```\n",
    'author': 'Eric Timmerman',
    'author_email': 'eric@tonic.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.tonic.ai/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
