from house_prices.data_processing import pipeline_train, split_train_test
from sklearn.linear_model import LinearRegression
import pickle


def build_model(df):

    xtrain, xtest, ytrain, ytest = split_train_test(df)
    xtrain = pipeline_train(xtrain)
    score = model(xtrain, ytrain)
    return score


def model(xtrain, ytrain):

    model = LinearRegression()
    model.fit(xtrain, ytrain)
    pickle.dump(model, open('../models/model.pickle', mode='wb'))
    score = model.score(xtrain, ytrain)
    return score
