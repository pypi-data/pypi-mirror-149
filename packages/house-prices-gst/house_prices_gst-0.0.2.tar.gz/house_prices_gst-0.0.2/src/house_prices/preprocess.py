import os
import joblib
import pandas as pd
import numpy as np
from datetime import date
from typing import Any, NoReturn, Tuple
from scipy.stats import skew
from sklearn.model_selection import train_test_split

SELECTED_FEATURES = [
    'GrLivArea', 'GarageArea', 'TotalBsmtSF', 'HouseStyle',
    'Neighborhood', 'OverallQual', 'ExterQual', 'KitchenQual', 'Functional',
    'FireplaceQu', 'YearsSinceBuilt', 'YearsSinceRemodAdd', 'BsmtExposure',
    'HalfBath', 'YearsSinceGarageYrBlt', 'Electrical', 'BsmtFullBath',
    'BldgType', 'KitchenAbvGr', 'Heating', 'CentralAir', 'GarageType',
    'GarageFinish', 'BsmtQual', 'SalePrice'
]

COLUMS_FOR_ORDINAL_ENCODING = [
    'BsmtQual', 'CentralAir', 'ExterQual', 'KitchenQual',
    'GarageFinish', 'Functional', 'FireplaceQu', 'BsmtExposure'
]
COLUMNS_FOR_ONE_HOT_ENCODING = [
    'HouseStyle', 'GarageType', 'Neighborhood', 'Heating',
    'Electrical', 'BldgType'
]

SELECTED_CONTINUOUS_FEATURES = [
    'GrLivArea', 'GarageArea', 'TotalBsmtSF',
    'YearsSinceBuilt', 'YearsSinceRemodAdd'
]
SELECTED_CATEGORICAL_FEATURES = [
    'HouseStyle', 'CentralAir', 'GarageType',
    'GarageFinish', 'Neighborhood', 'OverallQual',
    'ExterQual', 'KitchenQual', 'Functional', 'FireplaceQu',
    'Heating', 'BsmtExposure', 'HalfBath', 'YearsSinceGarageYrBlt',
    'Electrical', 'BsmtFullBath', 'BldgType', 'KitchenAbvGr', 'BsmtQual'
]

TARGET_FEATURE = 'SalePrice'

MODEL_FILENAME = 'model.joblib'
ORDINAL_ENCODER_FILENAME = 'ordinal_encoder.joblib'
ONE_HOT_ENCODER_FILENAME = 'one_hot_encoder.joblib'
STANDARD_SCALER_FILENAME = 'standard_scaler.joblib'
CONTINUOUS_FEATURES_MEANS_FILENAME = 'continuous_features_means.joblib'


def save_object(obj: Any, filename: str) -> NoReturn:
    current_working_dir = os.path.abspath(os.getcwd())
    file_path = os.path.join(
        os.path.dirname(current_working_dir),
        'models',
        filename
    )
    joblib.dump(obj, file_path)


def load_object(filename: str) -> Any:
    current_working_dir = os.path.abspath(os.getcwd())
    file_path = os.path.join(
        os.path.dirname(current_working_dir),
        'models',
        filename
    )
    obj = joblib.load(file_path)
    return obj


def fix_data_type(data: pd.DataFrame) -> pd.DataFrame:
    fixed_data = data.astype({
        "MSSubClass": object,
        "OverallQual": object,
        "OverallCond": object,
        "MoSold": object,
        "YrSold": object,
        "YearBuilt": object,
        "YearRemodAdd": object,
        "BsmtFullBath": object,
        "BsmtHalfBath": object,
        "FullBath": object,
        "HalfBath": object,
        "BedroomAbvGr": object,
        "KitchenAbvGr": object,
        "TotRmsAbvGrd": object,
        "Fireplaces": object,
        "GarageYrBlt": object,
        "GarageCars": object
    })
    return fixed_data


def update_data_features(data_raw: pd.DataFrame) -> pd.DataFrame:
    # Create additional features for better predictions
    todays_date = date.today()
    data_raw['YearsSinceBuilt'] = todays_date.year - data_raw['YearBuilt']
    data_raw['YearsSinceRemodAdd'] = \
        todays_date.year - data_raw['YearRemodAdd']
    data_raw['YearsSinceGarageYrBlt'] = \
        todays_date.year - data_raw['GarageYrBlt']
    return data_raw[SELECTED_FEATURES]


def clean_data(data_raw: pd.DataFrame) -> pd.DataFrame:
    fixed_type_data_raw = fix_data_type(data_raw)
    updated_data_raw = update_data_features(fixed_type_data_raw)
    return updated_data_raw


def split_train_data_raw(
        train_data_raw: pd.DataFrame
        ) -> Tuple[pd.DataFrame, pd.DataFrame]:
    y = train_data_raw[TARGET_FEATURE]
    X = train_data_raw.drop(TARGET_FEATURE, axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=0
    )

    train_data = pd.concat([X_train, y_train], axis=1)
    test_data = pd.concat([X_test, y_test], axis=1)

    return train_data, test_data


def handling_missing_data(data: pd.DataFrame) -> pd.DataFrame:
    continuous_features_means = load_object(CONTINUOUS_FEATURES_MEANS_FILENAME)
    data.loc[:, 'GrLivArea'] = \
        data.loc[:, 'GrLivArea'].fillna(continuous_features_means['GrLivArea'])
    data.loc[:, 'GarageArea'] = data.loc[:, 'GarageArea']\
        .fillna(continuous_features_means['GarageArea'])
    data.loc[:, 'TotalBsmtSF'] = data.loc[:, 'TotalBsmtSF']\
        .fillna(continuous_features_means['TotalBsmtSF'])
    data.loc[:, 'HouseStyle'] = data.loc[:, 'HouseStyle'].fillna('No')
    data.loc[:, 'Neighborhood'] = data.loc[:, 'Neighborhood']\
        .fillna('No')
    data.loc[:, 'OverallQual'] = data.loc[:, 'OverallQual']\
        .fillna(0).astype(object)
    data.loc[:, 'ExterQual'] = data.loc[:, 'ExterQual'].fillna('No')
    data.loc[:, 'KitchenQual'] = data.loc[:, 'KitchenQual'].fillna('No')
    data.loc[:, 'Functional'] = data.loc[:, 'Functional'].fillna('No')
    data.loc[:, 'FireplaceQu'] = \
        data.loc[:, 'FireplaceQu'].fillna('No')
    data.loc[:, 'YearsSinceRemodAdd'] = data.loc[:, 'YearsSinceRemodAdd']\
        .fillna(0)
    data.loc[:, 'YearsSinceBuilt'] = data.loc[:, 'YearsSinceBuilt'].fillna(0)
    data.loc[:, 'BsmtExposure'] = data.loc[:, 'BsmtExposure'].fillna('No')
    data.loc[:, 'HalfBath'] = data.loc[:, 'HalfBath']\
        .fillna(0).astype(object)
    data.loc[:, 'YearsSinceGarageYrBlt'] = \
        data.loc[:, 'YearsSinceGarageYrBlt'].fillna(0)
    data.loc[:, 'Electrical'] = data.loc[:, 'Electrical']\
        .fillna('No')
    data.loc[:, 'BsmtFullBath'] = data.loc[:, 'BsmtFullBath']\
        .fillna(0).astype(object)
    data.loc[:, 'BldgType'] = data.loc[:, 'BldgType'].fillna('No')
    data.loc[:, 'KitchenAbvGr'] = data.loc[:, 'KitchenAbvGr']\
        .fillna(0).astype(object)
    data.loc[:, 'Heating'] = data.loc[:, 'Heating'].fillna('No')
    data.loc[:, 'CentralAir'] = data.loc[:, 'CentralAir'].fillna('No')
    data.loc[:, 'GarageType'] = data.loc[:, 'GarageType'].fillna('No')
    data.loc[:, 'GarageFinish'] = data.loc[:, 'GarageFinish'].fillna('No')
    data.loc[:, 'BsmtQual'] = data.loc[:, 'BsmtQual'].fillna('No')
    return data


def fix_skewness(continuous_data: pd.DataFrame) -> pd.DataFrame:
    # Transform the continuous features with the skewness of more than 0.5
    skewness = continuous_data.apply(lambda x: skew(x))
    skewness = skewness[abs(skewness) > 0.5]
    skewed_features = skewness.index
    continuous_data[skewed_features] = \
        np.log1p(continuous_data[skewed_features].astype(float))
    return continuous_data


def transform_ordinal_encoding_features(
        categorical_data: pd.DataFrame,
        colums_for_ordinal_encoding: list[str]
        ) -> pd.DataFrame:
    ordinal_encoder = load_object(ORDINAL_ENCODER_FILENAME)
    categorical_data[colums_for_ordinal_encoding] = ordinal_encoder.transform(
        categorical_data[colums_for_ordinal_encoding]
    )
    return categorical_data


def transform_one_hot_encoding_features(
        categorical_data: pd.DataFrame,
        columns_for_one_hot_encoding: list[str]
        ) -> pd.DataFrame:
    one_hot_encoder = load_object(ONE_HOT_ENCODER_FILENAME)
    one_hot_encoder_columns = one_hot_encoder.get_feature_names_out()
    categorical_data.loc[:, one_hot_encoder_columns] = \
        one_hot_encoder.transform(
            categorical_data[columns_for_one_hot_encoding]
        ).toarray()
    categorical_data.drop(columns_for_one_hot_encoding, axis=1, inplace=True)
    return categorical_data


def transform_scaling_features(
        data: pd.DataFrame,
        continuous_features: list[str]
        ) -> pd.DataFrame:
    standard_scaler = load_object(STANDARD_SCALER_FILENAME)
    data.loc[:, continuous_features] = standard_scaler.transform(
        data.loc[:, continuous_features]
    )
    return data


def transform_features(
        data: pd.DataFrame, target_feature: str,
        categorical_features: list[str], continuous_features: list[str],
        colums_for_ordinal_encoding: list[str],
        columns_for_one_hot_encoding: list[str]
        ) -> Tuple[pd.DataFrame, Any]:
    y = np.log1p(data[target_feature]) if target_feature else None
    data_categorical = data[categorical_features]
    data_continuous = data[continuous_features]
    data_continuous = fix_skewness(data_continuous)
    data_categorical = transform_ordinal_encoding_features(
        data_categorical, colums_for_ordinal_encoding
    )
    data_categorical = transform_one_hot_encoding_features(
        data_categorical, columns_for_one_hot_encoding
    )
    data_continuous = transform_scaling_features(
        data_continuous,
        continuous_features
    )
    X = pd.concat([data_continuous, data_categorical], axis=1)
    return X, y


def predict(data: pd.DataFrame, model_filename: str) -> np.ndarray:
    model = load_object(model_filename)
    y_pred = model.predict(data)
    return y_pred
