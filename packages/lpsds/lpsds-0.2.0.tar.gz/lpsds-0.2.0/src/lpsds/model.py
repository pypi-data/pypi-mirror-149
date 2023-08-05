"""
Tools for model handling
"""

from sklearn.metrics import mean_squared_error
import numpy as np


def get_operation_model(model, X, y, metric=mean_squared_error, **kargv):
    """
    def get_operation_model(model, X, y, metric=mean_squared_error, *argv)

    Selects an operation model by running the entire dataset for each fold
    and picking the one with the best metric.

    The function always assume that the best value for a metric is its minimum value
    (MSE, for instance). If you use a metric like R2, where the higher the better, you must
    multiply such metric by -1.

    Input parameters:
        - model: a model structure as returned by sklearn cross_validation.
        - X: the input dataset
        - y: the target values
        - metric: a metric to be used (MSE, R2, etc.)
        - **kargv: passed down to the metric function.
    """
    res = np.array([metric(y, mod.predict(X), **kargv) for mod in model['estimator']])
    op_idx = np.argmin(res)
    return model['estimator'][op_idx]


def create_validation_dataset(model, X, y, proba: bool=True, copy: bool=True):
    """
    def create_validation_dataset(model, X, y, proba: bool=True, copy: bool=True)

    Create a validation dataset suitable for validate your model
    when deployed to another operation environment.

    Input parameters are:
        - model: a sklearn-like model (pipeline, skorch, etc.)
        - X: the input dataset
        - y: the targets of X
        - proba: if True, will call model.predict_proba. Otherwise, model.predict
        - copy: whether to return a copy of the passed dataset.
    
    Returns:
        A new dataset containing 2 new columns:
            - y_true: containing the targets in y.
            - y_pred: the model output for each sample in X.
    """

    if copy: df = X.copy()
    df['y_true'] = y
    df['y_pred'] = model.predict_proba(X) if proba else model.predict(X)
    return df
