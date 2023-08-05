from house_prices.data_processing import pipeline_test
import pickle
import pandas as pd


def make_prediction(df):

    df_id = df["Id"]
    df = pipeline_test(df)
    model = pickle.load(open('../models/model.pickle', mode='rb'))
    ypred = model.predict(df)
    result = pd.DataFrame(columns=["ID", "SalePrice"])
    result["ID"] = df_id
    result["SalePrice"] = ypred
    return result
