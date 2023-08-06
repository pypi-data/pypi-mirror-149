from typing import Tuple, List

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer


def make_data_transformer(
    data: pd.DataFrame,
    numeric_columns: List[str],
    categorical_columns: List[str],
    numeric_transformer_cls=MinMaxScaler,
    categorical_transformer_cls=OneHotEncoder,
) -> ColumnTransformer:
    """Factory for ColumnTransformer"""
    transformer_list = []
    if numeric_transformer_cls != "passthrough":
        transformer = numeric_transformer_cls()
    else:
        transformer = "passthrough"
    transformer_list.append(("Numeric", transformer, numeric_columns))

    if categorical_transformer_cls == OneHotEncoder:
        transformer = OneHotEncoder(sparse=False, handle_unknown="ignore")
    else:
        transformer = categorical_transformer_cls(
            handle_unknown="use_encoded_value", unknown_value=-1
        )
    transformer_list.append(("Categorical", transformer, categorical_columns))
    column_transformer = ColumnTransformer(
        transformers=transformer_list, remainder="drop"
    )
    column_transformer.fit(data)
    return column_transformer


def filter_null_and_match_row_counts(real_data, synth_data, cols):
    num_null_values = real_data[cols].isna().sum().sum()
    if num_null_values > 0:
        real_data = real_data.dropna(subset=cols)
        synth_data = synth_data.head(len(real_data))
        print(
            str(num_null_values)
            + " null values found across columns "
            + ", ".join(cols)
            + ". Removing rows with null values and limiting synthesized row count to non-null real data row count."
        )

    return real_data, synth_data
