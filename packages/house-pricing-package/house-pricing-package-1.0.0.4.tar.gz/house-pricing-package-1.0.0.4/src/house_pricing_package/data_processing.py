
import re
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_log_error
pd.options.mode.chained_assignment = None


def split_train_test(df):

    X = df.iloc[:, :-1]
    Y = df.iloc[:, -1]
    xtrain, xtest, ytrain, ytest = train_test_split(X,
                                                    Y,
                                                    test_size=0.30,
                                                    random_state=42)
    return xtrain, xtest, ytrain, ytest


def feature_selection(df):

    feature_selected = ["Neighborhood",
                        "LotArea",
                        "Utilities",
                        "OverallQual",
                        "YearBuilt",
                        "GrLivArea",
                        "ExterCond",
                        "1stFlrSF",
                        "TotRmsAbvGrd",
                        "KitchenQual"]

    df = df[feature_selected]
    return df


def divide_by_type(df):

    cat_features = [features for features in df.columns
                    if df[features].dtype == "O"]
    num_features = [features for features in df.columns
                    if df[features].dtype != "O"]
    date_features = [features for features in df.columns if "Yr" in features
                     or "Year" in features
                     or "Mo" in features]
    features = []
    for feature in num_features:
        if feature not in date_features:
            features.append(feature)
    num_features = features
    return cat_features, num_features, date_features


def divide_ord_features(df, cat_features, num_features):

    num_max = df[num_features].max()
    ord_num_features = num_max[num_max <= 15].index.tolist()
    ordinal_features = [features for features in df.columns
                        if re.search('Qu$', features)
                        or re.search('QC', features)
                        or re.search('Qual$', features)
                        or re.search('Cond$', features)]

    ord_cat_features = [features for features in ordinal_features
                        if df[features].dtype == "O"]
    return (ordinal_features,
            ord_num_features,
            ord_cat_features)


def update_cat_and_num_features(num_features,
                                cat_features,
                                features_to_rmv):

    update_numerical = []
    for feature in num_features:
        if feature not in (features_to_rmv):
            update_numerical.append(feature)

    update_categorical = []
    for feature in cat_features:
        if feature not in features_to_rmv:
            update_categorical.append(feature)

    return update_numerical, update_categorical


def fill_numerical_missing_values(df, num_features):
    df_numerical = df[num_features].fillna(0)
    return df_numerical


def fit_scaler_min_max(df, num_features):
    scaler = MinMaxScaler()
    scaler.fit(df[num_features])
    pickle.dump(scaler, open('../models/MinMax_Numerical_scaler.pickle', 'wb'))
    return scaler


def transform_scaler_min_max(df, num_features):

    scaler = pickle.load(open('../models/MinMax_Numerical_scaler.pickle',
                              'rb'))
    df[num_features] = scaler.transform(df[num_features])

    return df


def fill_missing_categorical_values(df, cat_features):

    for feature in cat_features:
        if df[feature].isnull().sum() == 1:
            df[feature] = df[feature].fillna(df[feature].mode())
        else:
            df[feature] = df[feature].fillna("Missing")
    return df[cat_features]


def fit_one_hot_encoding(df, cat_features):

    enc = OneHotEncoder(handle_unknown="ignore", sparse=False)
    enc.fit(df[cat_features])
    pickle.dump(enc, open('../models/One_Hot_Encoder.pickle', 'wb'))

    return enc


def transform_one_hot(df, cat_features):

    enc = pickle.load(open('../models/One_Hot_Encoder.pickle', 'rb'))
    values = enc.transform(df[cat_features])
    names = enc.get_feature_names_out(df[cat_features].columns)
    df1 = pd.DataFrame(columns=names)
    df = pd.concat([df, df1], axis=1)
    df[names] = values
    df = df.drop(cat_features, axis=1)
    return df


def fill_missing_ord_num_values(df, ord_num_features):

    df_num_ordinal = df[ord_num_features]
    if np.sum(df_num_ordinal.isnull().sum() > 0):
        df_num_ordinal = df_num_ordinal.fillna(0)

    return df_num_ordinal


def fit_scaler_ordinal_numerical(df, ord_num_features):

    file = '../models/MinMax_Ordinal_Numerical_scaler.pickle'
    scaler = MinMaxScaler()
    scaler.fit(df[ord_num_features])
    pickle.dump(scaler, open(
                              file,
                              'wb'))
    return scaler


def transform_ordina_num_features(df, ord_num_features):

    file = '../models/MinMax_Ordinal_Numerical_scaler.pickle'
    df_num_ord = df[ord_num_features]
    scaler = pickle.load(open(file,  mode='rb'))
    df[ord_num_features] = (scaler.transform(
                                                        df_num_ord
                                                        ))
    return df


def fill_missing_ord_cat_values(df, ord_cat_features):

    for feature in ord_cat_features:
        if df[feature].isnull().sum() == 1:
            df[feature] = df[feature].fillna(df[feature].mode())
        else:
            df[feature] = df[feature].fillna("Missing")
    return df[ord_cat_features]


def fit_ordinal_categorical(df, ord_cat_features):

    enc = OrdinalEncoder(
                       handle_unknown="use_encoded_value",
                       unknown_value=6
    )
    enc.fit(df[ord_cat_features])
    pickle.dump(enc,  open('../models/Ordinal_Encoder.pickle', "wb"))
    return enc


def transform_ord_cat_features(df, ord_cat_features):

    df_cat_ord = df[ord_cat_features]
    enc = pickle.load(open('../models/Ordinal_Encoder.pickle', "rb"))
    df[ord_cat_features] = enc.transform(df_cat_ord)
    return df


def fit_scaler_ordinal_categorical(df, ord_cat_features):

    scaler = MinMaxScaler()
    file = '../models/MinMax_Ordinal_Categorical_scaler.pickle'
    scaler.fit(df[ord_cat_features])
    pickle.dump(scaler,  open(file,  mode='wb'))
    return scaler


def transform_scaler_ordinal_categorical(df, ord_cat_features):

    df_cat_ord = df[ord_cat_features]
    file = '../models/MinMax_Ordinal_Categorical_scaler.pickle'
    scaler = pickle.load(open(file,  mode='rb'))
    df[ord_cat_features] = scaler.transform(df_cat_ord)
    return df


def fill_missing_dates_values(df, date_features):

    for features in date_features:
        df[features] = df[features].fillna(df[features].mode())

    return df[date_features]


def fit_scaler_dates(df, date_features):

    scaler = MinMaxScaler()
    file = '../models/MinMax_dates_scaler.pickle'
    scaler.fit(df[date_features])
    pickle.dump(scaler,  open(file,  mode='wb'))
    return scaler


def transform_dates(df, date_features):

    file = '../models/MinMax_dates_scaler.pickle'
    scaler = pickle.load(open(file,  mode='rb'))
    df[date_features] = scaler.transform(df[date_features])
    return df


def pipeline_train_num_features(df, num_features):

    numerical_null = fill_numerical_missing_values(df, num_features)
    df.loc[:, num_features] = numerical_null
    fit_scaler_min_max(df, num_features)
    df = transform_scaler_min_max(df, num_features)
    return df


def pipeline_train_categorical_feature(df, cat_features):

    df[cat_features] = fill_missing_categorical_values(df, cat_features)
    fit_one_hot_encoding(df, cat_features)
    df = transform_one_hot(df, cat_features)
    return df


def pipeline_train_ord_num_features(df, ord_num_features):

    df[ord_num_features] = fill_missing_ord_num_values(df, ord_num_features)
    fit_scaler_ordinal_numerical(df, ord_num_features)
    df = transform_ordina_num_features(df, ord_num_features)
    return df


def pipeline_train_ord_cat_features(df, ord_cat_features):

    df[ord_cat_features] = fill_missing_ord_cat_values(df, ord_cat_features)
    fit_ordinal_categorical(df, ord_cat_features)
    df = transform_ord_cat_features(df, ord_cat_features)
    fit_scaler_ordinal_categorical(df, ord_cat_features)
    df = transform_scaler_ordinal_categorical(df, ord_cat_features)
    return df


def pipeline_train_dates_features(df, date_features):

    df[date_features] = fill_missing_dates_values(df, date_features)
    fit_scaler_dates(df, date_features)
    df = transform_dates(df, date_features)
    return df


def splitting_types(df):

    df = feature_selection(df)
    cat_features, num_features, date_features = divide_by_type(df)
    (ordinal_features,
     ord_num_features,
     ord_cat_features) = divide_ord_features(df, cat_features, num_features)
    features_to_rmv = ord_cat_features+ord_num_features
    num_features, cat_features = update_cat_and_num_features(num_features,
                                                             cat_features,
                                                             features_to_rmv)
    return (num_features,
            cat_features,
            ordinal_features,
            ord_num_features,
            ord_cat_features,
            date_features,
            df)


def pipeline_train(df):

    (num_features,
     cat_features,
     ordinal_features,
     ord_num_features,
     ord_cat_features,
     date_features,
     df) = splitting_types(df)
    df = pipeline_train_num_features(df, num_features)
    df = pipeline_train_categorical_feature(df, cat_features)
    df = pipeline_train_ord_num_features(df, ord_num_features)
    df = pipeline_train_ord_cat_features(df, ord_cat_features)
    df = pipeline_train_dates_features(df, date_features)
    return df

# Test


def pipeline_test_num_features(df, num_features):

    numerical_null = fill_numerical_missing_values(df, num_features)
    df.loc[:, num_features] = numerical_null
    df = transform_scaler_min_max(df, num_features)
    return df


def pipeline_test_categorical_feature(df, cat_features):

    df[cat_features] = fill_missing_categorical_values(df, cat_features)
    df = transform_one_hot(df, cat_features)
    return df


def pipeline_test_ord_num_features(df, ord_num_features):

    df[ord_num_features] = fill_missing_ord_num_values(df, ord_num_features)
    df = transform_ordina_num_features(df, ord_num_features)
    return df


def pipeline_test_ord_cat_features(df, ord_cat_features):

    df[ord_cat_features] = fill_missing_ord_cat_values(df, ord_cat_features)
    df = transform_ord_cat_features(df, ord_cat_features)
    df = transform_scaler_ordinal_categorical(df, ord_cat_features)
    return df


def pipeline_test_dates_features(df, date_features):

    df[date_features] = fill_missing_dates_values(df, date_features)
    df = transform_dates(df, date_features)
    return df


def pipeline_test(df):

    (num_features,
     cat_features,
     ordinal_features,
     ord_num_features,
     ord_cat_features,
     date_features,
     df) = splitting_types(df)
    df = pipeline_test_num_features(df, num_features)
    df = pipeline_test_categorical_feature(df, cat_features)
    df = pipeline_test_ord_num_features(df, ord_num_features)
    df = pipeline_test_ord_cat_features(df, ord_cat_features)
    df = pipeline_test_dates_features(df, date_features)
    return df


def compute_rmsle(y_test, y_pred, precision: int = 2) -> float:
    rmsle = np.sqrt(mean_squared_log_error(y_test,  y_pred))
    return round(rmsle,  precision)
