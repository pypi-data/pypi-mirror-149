"""
    These are some kits for TechLearning
    机器学习工具集
"""
import os
import random
import numpy as np
from sklearn import datasets
# 导入KNN分类器
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler


def GetKNNSoreByN(X, y, n_neighbors):
    """
    :param X: data 特征值
    :param y: aim 目标值
    :param n_neighbors K值
    :return: score 预测结果
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    transform = StandardScaler()
    X_train = transform.fit_transform(X_train)
    X_test = transform.fit_transform(X_test)
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(X_train, y_train)
    y_pre = clf.predict(X_test)
    return sum(y_pre == y_test) / y_pre.shape[0]


def GetKNNScoreByGridSearchCV(X, y, param_grid: dict = {'n_neighbors': [i for i in range(1, 10, 1)]}):
    """
    :param X:data 特征值
    :param y:aim 目标值
    :param param_grid: GridSearchCV param 传递给GridSearchCV的参数
    :return: best params and best score for KNN最好的参数表以及最佳准确率
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    transform = StandardScaler()
    X_train = transform.fit_transform(X_train)
    X_test = transform.fit_transform(X_test)
    estimator = KNeighborsClassifier()
    estimator = GridSearchCV(estimator, param_grid=param_grid, cv=5, verbose=0)
    estimator.fit(X_train, y_train)

    return estimator.best_params_, estimator.best_score_


def linear_model_regular(data):
    """
    regular 正则
    :param data: data 数据
    :return: coef 系数列表, intercept 截距, error 均方误差
    """
    x_train, x_test, y_train, y_test = train_test_split(data.data, data.target, random_state=0)
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)
    estimator = LinearRegression()
    estimator.fit(x_train, y_train)
    y_predict = estimator.predict(x_test)
    error = mean_squared_error(y_test, y_predict)  # 均方误差

    return estimator.coef_, estimator.intercept_, error


def linear_model_gradient(data):
    """
    gradient descent 梯度下降
    :param data: data 数据
    :return: coef 系数列表, intercept 截距, error 均方误差
    """
    x_train, x_test, y_train, y_test = train_test_split(data.data, data.target, random_state=0)
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)
    estimator = SGDRegressor(max_iter=1000)
    estimator.fit(x_train, y_train)
    y_predict = estimator.predict(x_test)
    error = mean_squared_error(y_test, y_predict)  # 均方误差

    return estimator.coef_, estimator.intercept_, error


def setup_module(module):
    """
    Prevent multiple uses of the same library
    """
    # Check if a random seed exists in the environment, if not create one.
    _random_seed = os.environ.get('SKLEARN_SEED', None)
    if _random_seed is None:
        _random_seed = np.random.uniform() * np.iinfo(np.int32).max
    _random_seed = int(_random_seed)
    print("I: Seeding RNGs with %r" % _random_seed)
    np.random.seed(_random_seed)
    random.seed(_random_seed)


if __name__ == '__main__':
    # 写在这里，其他人不会调用
    # X, y = datasets.load_iris(return_X_y=True)
    # param_grid = {'n_neighbors': [1, 3, 5, 7]}
    # print(GetKNNSoreByN(X, y, 3))
    # print(GetKNNScoreByGridSearchCV(X, y, param_grid=param_grid))
    # print(GetKNNScoreByGridSearchCV(X, y))
    data = load_boston()
    coef_, intercept_, error = linear_model_gradient(data=data)
    print("模型中的系数为:\n", coef_)
    print("模型中的偏置为:\n", intercept_)
    print("误差为:\n", error)
