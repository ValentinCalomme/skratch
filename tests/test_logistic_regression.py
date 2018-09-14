import pytest
import sys

import numpy as np

import supervised.logistic_regression as skratch

from utils.optimization import StochasticGradientDescentOptimizer
from utils.preprocessing import add_dummy_feature, StandardScaler
from utils.activation import Sigmoid

EPSILON = 5E-2

n_samples = range(10, 400, 10)
n_features = range(1, 10)

sigmoid = Sigmoid()


def get_X_y_weights(n_samples, n_features, fit_intercept):

    X = np.random.rand(n_samples, n_features)
    weights = np.random.rand(X.shape[1] + fit_intercept)
    X = StandardScaler().fit_transform(X)

    features = X
    if fit_intercept:
        features = add_dummy_feature(features)

    y = sigmoid(features.dot(weights)) > 0.5

    return X, y, weights


@pytest.mark.parametrize("n_samples", n_samples)
@pytest.mark.parametrize("n_features", n_features)
@pytest.mark.parametrize("fit_intercept", [0, 1])
def test_linear_regression(n_samples, n_features, fit_intercept):

    X, y, weights = get_X_y_weights(n_samples, n_features, fit_intercept)

    reg = skratch.LogisticRegression(fit_intercept=fit_intercept)
    optimizer = StochasticGradientDescentOptimizer()

    reg.optimizer = optimizer
    reg.fit(X, y)
    r0 = reg.predict(X)

    error_r0 = np.mean((r0 == y))

    assert error_r0 < EPSILON
