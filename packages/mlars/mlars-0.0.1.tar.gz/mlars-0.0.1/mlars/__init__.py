import pandas as pd
import numpy as np
from sklearn import *
from colorama import Fore, Back, Style
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import datasets, metrics, neighbors,  linear_model, svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB

from mars.getData import clearData, getData
# from xgboost import XGBClassifier

models = [
    ["SVM",lambda nu: linear_model.SGDOneClassSVM(nu=nu), [
         [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
         [True, False],
         [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
         [0.001, 0.01, 0.1, 1, 10, 100, 1000],
         [True, False],
         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
         [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
         ["constant", "optimal", "invscaling", "adaptive"],
         [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
         [True, False],
         [False, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    ]],
    ["logistic Regression",lambda penalty:  linear_model.LogisticRegression(penalty= penalty,max_iter=10000), [
        [ 'l2',  'none'],
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [True, False],
        [0.001, 0.01, 0.1, 1, 10, 100, 1000],
        [True, False],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ["balanced", "balanced_subsample", ],
        [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ["newton-cg", "lbfgs", "liblinear", "sag", "saga"],
        [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
        ["ovr", "multinomial"],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [True, False],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    ]],
    ["Random Forest",lambda n_estimators : RandomForestClassifier(n_estimators=n_estimators), [
        [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        ["gini", "entropy"],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [2, 3, 4, 5, 6, 7, 8, 9, 10],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        ["auto", "sqrt", "log2"],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [True, False],
        [True, False],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [True, False],
        ["balanced", "balanced_subsample", ],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    ]],
    ["Gaussian Naive Bayes",lambda var_smoothing:  GaussianNB(var_smoothing=var_smoothing),
     [

         [1e-09, 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 1e-02, 1e-01, 1.0],
         [None, [0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [
             0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]],
     ]
     ],
    ["KNN", lambda n_neighbors :  neighbors.KNeighborsClassifier(n_neighbors=n_neighbors), [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ["uniform", "distance"],
        ["auto", "ball_tree", "kd_tree", "brute"],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ["euclidean", "minkowski", "manhattan", "chebyshev",
         "mahalanobis", "seuclidean", "wminkowski", "mahalanobis"],
        [None, {"p": 1, "V": None}, {"p": 2, "V": None}, {"p": 3, "V": None}, {"p": 1, "V": None}, {"V": None}, {
            "p": 1, "V": None}, {"p": 1, "V": None}, {"p": 1, "V": None}, {"p": 1, "V": None}, {"p": 1, "V": None}],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    ], ],
    ["Decision Tree",lambda criterion :  DecisionTreeClassifier(criterion=criterion), [
        ["gini", "entropy"],
        ["best", "random"],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [2, 3, 4, 5, 6, 7, 8, 9, 10],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        ["auto", "sqrt", "log2"],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ["balanced", "balanced_subsample", ],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    ]],
    # this doesn't work
    ["Multinomial Naive Bayes", lambda alpha : MultinomialNB(alpha=alpha), [
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [True, False],
        [None, [0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [
            0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]],
    ]],
    ["Bernoulli Naive Bayes",lambda alpha:  BernoulliNB(alpha=alpha),  [
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [True, False],
        [None, [0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [
            0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]],
    ]],
    ["AdaBoost",lambda base_estimator: AdaBoostClassifier(base_estimator=base_estimator,), 
     [
         [None, DecisionTreeClassifier(), GaussianNB(),
        #   MultinomialNB(),
          BernoulliNB()],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
         [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
         ["SAMME", "SAMME.R"],
         [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
     ],],
    ["Gradient Boosting",lambda learning_rate : GradientBoostingClassifier(learning_rate=learning_rate), [
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        ["deviance", "exponential"],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0.5, 0.6, 0.7, 0.8, 0.9, 1],
        ["friedman_mse", "mse", "mae"],
        [2, 3, 4, 5, 6, 7, 8, 9, 10],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [None, "zero"],
        [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ["auto", "sqrt", "log2"],
        [0, 1],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [True, False],
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [0.0001, 0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],

    ]],
    ["Extra Trees",lambda n_estimators: ExtraTreesClassifier(n_estimators=n_estimators), [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ["gini", "entropy"],
        ["auto", "sqrt", "log2"],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [2, 3, 4, 5, 6, 7, 8, 9, 10],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [None, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [True, False],
        [True, False],
        [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0, 1],
        [True, False],
        [None, "balanced"],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [0.5, 0.6, 0.7, 0.8, 0.9, 1],

    ]],
    ]
    # ["XGBoost", XGBClassifier]



def main (df, name: str , min: int = 103):
    df = clearData(df)
    unique = df[name].unique()
    print(Fore.YELLOW + "starting with dataframe of shape: {} {}".format(df.shape[0], df.shape[1])
          + "\nand the column is:", name
          + "\nwith {0} unique values , {1} and {2}".format(len(unique), unique[0], unique[1]))
    data = getData(df, name, unique)
    print(Fore.GREEN + "train test split done test size: {}".format(0.2))
    print(Fore.YELLOW + "training model")
    print (Fore.YELLOW + "new shape of train data: {} {}".format(data[0].shape[0], data[0].shape[1]))
    bestaccuracy = 0
    for item in models:
        for param in item[2][0]:
            try:
                print(Fore.CYAN + item[0] , end=" ")
                model = getModel(data[0], data[2], item[1],param )
                y = getPredictions(model, data[1])
                accuracy = getAccuracy(data[3], y)
                if accuracy*100 >= min:
                    bestmodelname = item[0]
                    bestaccuracy = accuracy
                    break
                if accuracy > bestaccuracy:
                    bestaccuracy = accuracy
                    bestmodelname = item[0]
                    bestmodel = model
            except:
                print(Fore.BLUE + "This Algorithm is not supported")
    print(Fore.YELLOW + "done")
    print(Fore.GREEN + "best model is: {} ,with accuracy {}".format(bestmodelname, bestaccuracy))
    return bestmodel


def getModel(X_train, y_train, Model, param):
    model = Model(param)
    model.fit(X_train, y_train)
    print(Fore.WHITE + "model fit done with params " + str(param) , end = ' ')
    return model


def getPredictions(model, X_test):
    predictions = model.predict(X_test)
    # print(Fore.GREEN + "predictions done")
    return predictions


def getAccuracy(y_test, predictions):
    accuracy = accuracy_score(y_test, predictions)
    print(Fore.BLUE + str(accuracy))
    return accuracy
