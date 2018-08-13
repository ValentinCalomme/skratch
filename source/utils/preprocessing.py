import itertools
import copy

import numpy as np

EPSILON = 1E-16


class Normalizer:

    def __init__(self, norm="l2"):

        self.norm_type = norm

    def fit(self, X):

        if self.norm_type == "l2":
            self.norm = np.sqrt(np.sum(X**2, axis=1))[:, None]

        elif self.norm_type == "l1":

            self.norm = np.sum(X**1, axis=1)[:, None]

        elif self.norm_type == "max":

            self.norm = np.max(X, axis=1)[:, None]

        return self

    def transform(self, X):

        X = copy.copy(X)

        return X / self.norm

    def fit_transform(self, X):

        return self.fit(X).transform(X)


class StandardScaler:

    def __init__(self, with_mean=True, with_std=True):

        self.with_mean = with_mean
        self.with_std = with_std

    def fit(self, X):

        if self.with_mean:
            self.mean = X.mean(axis=0)

        if self.with_std:
            self.std = X.std(axis=0)

        return self

    def transform(self, X):

        X = copy.copy(X)

        if self.with_mean:
            X -= self.mean

        if self.with_std:
            X /= self.std

        return X

    def fit_transform(self, X):

        return self.fit(X).transform(X)


class MinMaxScaler:

    def __init__(self, feature_range=(0, 1)):

        self.min_value, self.max_value = feature_range

    def fit(self, X):

        self.min = X.min(axis=0)
        self.max = X.max(axis=0)

        return self

    def transform(self, X):

        X = copy.copy(X)

        X = (X - self.min) / (self.max - self.min)
        X = X * (self.max_value - self.min_value) + self.min_value

        return X

    def fit_transform(self, X):

        return self.fit(X).transform(X)


class MaxAbsScaler:

    def fit(self, X):

        self.abs_max = np.max(np.abs(X), axis=0)

        return self

    def transform(self, X):

        X = copy.copy(X)

        return np.divide(X, self.abs_max)

    def fit_transform(self, X):

        return self.fit(X).transform(X)


def polynomial_features(X, degree=1):

    poly = []

    for x in X:

        features = []
        for i in range(1, degree + 1):

            for combi in itertools.combinations_with_replacement(x, i):
                features.append(np.product(combi))

        poly.append(features)

    return np.array(poly)


def add_dummy_feature(X, value=1.0):

    X = copy.copy(X)

    n_samples, _ = X.shape
    offset = np.full((n_samples, 1), fill_value=value)

    return np.concatenate((offset, X), axis=1)


def binarize(X, threshold=0.0):

    return X > threshold
