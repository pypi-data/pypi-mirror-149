import numpy as np
import pandas as pd
from house_prices.preprocess import (
    clean_data, handling_missing_data, predict, transform_features
)
from house_prices.preprocess import (
    MODEL_FILENAME, SELECTED_CATEGORICAL_FEATURES,
    SELECTED_CONTINUOUS_FEATURES, COLUMS_FOR_ORDINAL_ENCODING,
    COLUMNS_FOR_ONE_HOT_ENCODING
)


def make_predictions(input_data_raw: pd.DataFrame) -> np.ndarray:
    # the model and all the data preparation objects (encoder, etc)
    # should be loaded from the models folder
    data = clean_data(input_data_raw)
    data = handling_missing_data(data)
    X, y = transform_features(
        data, None, SELECTED_CATEGORICAL_FEATURES,
        SELECTED_CONTINUOUS_FEATURES, COLUMS_FOR_ORDINAL_ENCODING,
        COLUMNS_FOR_ONE_HOT_ENCODING
    )
    y_pred = predict(X, MODEL_FILENAME)
    return np.expm1(y_pred)
