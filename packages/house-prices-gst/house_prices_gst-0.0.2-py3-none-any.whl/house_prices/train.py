import pandas as pd
import numpy as np
from typing import Any, NoReturn
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_log_error
from house_prices.preprocess import (
    save_object, clean_data, split_train_data_raw, handling_missing_data,
    transform_features, predict
)
from house_prices.preprocess import (
    ORDINAL_ENCODER_FILENAME, ONE_HOT_ENCODER_FILENAME,
    SELECTED_CATEGORICAL_FEATURES, STANDARD_SCALER_FILENAME,
    MODEL_FILENAME, TARGET_FEATURE,
    CONTINUOUS_FEATURES_MEANS_FILENAME, SELECTED_CONTINUOUS_FEATURES,
    COLUMNS_FOR_ONE_HOT_ENCODING, COLUMS_FOR_ORDINAL_ENCODING
)


def compute_rmsle(
        y_test: np.ndarray,
        y_pred: np.ndarray,
        precision: int = 2
        ) -> dict[str, str]:
    rmsle = np.sqrt(mean_squared_log_error(y_test, y_pred))
    return {'rmsle': f"{round(rmsle, precision)}"}


def fit_ordinal_encoding_features(
        categorical_data: pd.DataFrame,
        colums_for_ordinal_encoding: list[str]
        ) -> NoReturn:
    ordinal_encoder = OrdinalEncoder(categories=[
        ["No", "Po", "Fa", "TA", "Gd", "Ex"],
        ["N", "Y"],
        ["No", "Po", "Fa", "TA", "Gd", "Ex"],
        ["No", "Po", "Fa", "TA", "Gd", "Ex"],
        ["No", "Unf", "RFn", "Fin"],
        ["No", "Sal", "Sev", "Maj2", "Maj1", "Mod", "Min2", "Min1", "Typ"],
        ["No", "Po", "Fa", "TA", "Gd", "Ex"],
        ["No", "Mn", "Av", "Gd"]
    ])
    ordinal_encoder.fit(categorical_data[colums_for_ordinal_encoding])
    save_object(ordinal_encoder, ORDINAL_ENCODER_FILENAME)


def fit_one_hot_encoding_features(
        categorical_data: pd.DataFrame,
        columns_for_one_hot_encoding: list[str]
        ) -> NoReturn:
    one_hot_encoder = OneHotEncoder()
    one_hot_encoder.fit(categorical_data[columns_for_one_hot_encoding])
    save_object(one_hot_encoder, ONE_HOT_ENCODER_FILENAME)


def fit_scaling_features(
        data: pd.DataFrame,
        continuous_features: list[str]
        ) -> NoReturn:
    # Scaling
    standard_scaler = StandardScaler()
    standard_scaler.fit(data.loc[:, continuous_features])
    save_object(standard_scaler, STANDARD_SCALER_FILENAME)


def fit_features(
        data: pd.DataFrame,
        categorical_features: list[str],
        continuous_features: list[str],
        colums_for_ordinal_encoding: list[str],
        columns_for_one_hot_encoding: list[str]
        ) -> NoReturn:
    data_categorical = data[categorical_features]
    data_continuous = data[continuous_features]
    fit_ordinal_encoding_features(
        data_categorical,
        colums_for_ordinal_encoding
    )
    fit_one_hot_encoding_features(
        data_categorical,
        columns_for_one_hot_encoding
    )
    fit_scaling_features(data_continuous, continuous_features)


def train_model(X: pd.DataFrame, y: np.ndarray) -> Any:
    # Train
    model = LinearRegression()
    model.fit(X, y)
    save_object(model, MODEL_FILENAME)
    return model


def build_model(data_raw: pd.DataFrame) -> dict[str, str]:
    # Returns a dictionary with the model
    # performances (for example {'rmse': 0.18})
    cleaned_data = clean_data(data_raw)
    train_data, test_data = split_train_data_raw(cleaned_data)
    # Calculate the mean of continuous features and saving them
    continuous_features_means = {
        'GrLivArea': np.mean(train_data['GrLivArea']),
        'GarageArea': np.mean(train_data['GarageArea']),
        'TotalBsmtSF': np.mean(train_data['TotalBsmtSF'])
    }
    save_object(continuous_features_means, CONTINUOUS_FEATURES_MEANS_FILENAME)
    # Handle missing data
    train_data = handling_missing_data(train_data)
    test_data = handling_missing_data(test_data)
    # Fit train data
    fit_features(
        train_data,
        SELECTED_CATEGORICAL_FEATURES, SELECTED_CONTINUOUS_FEATURES,
        COLUMS_FOR_ORDINAL_ENCODING, COLUMNS_FOR_ONE_HOT_ENCODING
    )
    # Transform train data and test data
    X_train, y_train = transform_features(
        train_data, TARGET_FEATURE,
        SELECTED_CATEGORICAL_FEATURES, SELECTED_CONTINUOUS_FEATURES,
        COLUMS_FOR_ORDINAL_ENCODING, COLUMNS_FOR_ONE_HOT_ENCODING
    )
    X_test, y_test = transform_features(
        test_data, TARGET_FEATURE,
        SELECTED_CATEGORICAL_FEATURES, SELECTED_CONTINUOUS_FEATURES,
        COLUMS_FOR_ORDINAL_ENCODING, COLUMNS_FOR_ONE_HOT_ENCODING
    )
    # Train model and predict
    train_model(X_train, y_train)
    y_pred = predict(X_test, MODEL_FILENAME)
    result = compute_rmsle(y_test, y_pred)
    return result
