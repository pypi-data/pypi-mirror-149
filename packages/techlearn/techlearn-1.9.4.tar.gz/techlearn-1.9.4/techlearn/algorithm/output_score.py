import numpy as np
from sklearn import datasets
# 导入KNN分类器
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def get_KNN_by_set(X,y,n_neighbors):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    transform = StandardScaler()
    X_train = transform.fit_transform(X_train)
    X_test = transform.fit_transform(X_test)
    clf = KNeighborsClassifier(n_neighbors=n_neighbors, p=2)
    clf.fit(X_train, y_train)
    y_pre = clf.predict(X_test)
    return sum(y_pre == y_test) / y_pre.shape[0]


if __name__ == '__main__':
    # 写在这里，其他人不会调用
    X,y = datasets.load_iris(return_X_y=True)
    print(get_KNN_by_set(X,y,3))

