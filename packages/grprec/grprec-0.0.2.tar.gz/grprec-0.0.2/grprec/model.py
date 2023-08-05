"""Module dedicated to model training and group scores predictions.

.. autosummary::
    :nosignatures:

    SVD_model
    predict_for_group
    predict_for_group2
"""
from surprise import Dataset, Reader, SVD, accuracy
import os
import pandas as pd
import numpy as np


def SVD_model(train, test, param_path, scores_scale, verbose=False):
    """Trains an `SVD` matrix factorisation model on the trainset using the parameters in the file path. Shows the `RMSE` on console if verbose is True. 

    Args:
        train: Pandas Dataframe containing a user column named `uid`, an item column named `iid`, and a ratings column named `rating`.
        test:Pandas Dataframe containing a user column named `uid`, an item column named `iid`, and a ratings column named `rating`.
        param_path: Path to the model hyper parameters.
        scores_scale: Scale of the ratings in the train and test sets. Ex: (0,5)
        verbose: If True, shows the `RMSE` on console ofter model fitting. False by default.

    Returns:
        The `SVD` fitted model.
    """
    reader = Reader(rating_scale=scores_scale)

    trainset = Dataset.load_from_df(train, reader).build_full_trainset()
    testset = Dataset.load_from_df(
        test, reader).build_full_trainset().build_testset()

    with open(param_path, 'r') as par:
        line = par.readline().strip('\n')
        params = line.split('\t')

    m = SVD(n_factors=int(params[0]), n_epochs=int(
        params[1]), lr_all=float(params[2]), reg_all=float(params[3]))
    m.fit(trainset)

    if(verbose == True):
        predictions = m.test(testset)
        accuracy.rmse(predictions, verbose=True)

    return(m)


def predict_for_group(model, group, list_items):
    """Predicts individual scores prediction for a group and a list of items by using the model.

    Args:
        model: The model used for score prediction.
        group: A list of users to predict for.
        list_items: A list of items to predict for every group member.

    Returns:
        A Pandas Dataframe as a matrix of dimension (|`group`|x|`list_items`|) containing score predictions.
    """
    scores = []
    users_idx = []
    for u in group:
        users_idx.append(u)
        user_predictions = []
        for i in list_items:
            user_predictions.append(model.predict(int(u), int(i))[3])
        scores.append(user_predictions)
    group_predictions = pd.DataFrame(
        np.array(scores), index=users_idx, columns=list_items)
    return group_predictions


def predict_for_group2(model, group, list_items, trainset):
    """Predicts individual scores prediction for a group and a list of items by using the model.
    If a user has already seen an item in the trainset, the score is set to 0 to discourage already seen items from being recommended.
    Args:
        model: The model used for score prediction.
        group: A list of users to predict for.
        list_items: A list of items to predict for every group member.
        trainset: Pandas Dataframe containing a user column named `uid`, an item column named `iid`, and a ratings column named `rating`.

    Returns:
        A Pandas Dataframe as a matrix of dimension (|`group`|x|`list_items`|) containing score predictions.
    """
    scores = []
    users_idx = []
    for u in group:
        users_idx.append(u)
        user_predictions = []
        rated_movies_by_user = trainset[(trainset.uid == int(u))].iid.unique()
        for i in list_items:
            if (int(i) in rated_movies_by_user):
                user_predictions.append(0)
            else:
                user_predictions.append(model.predict(int(u), int(i))[3])
        scores.append(user_predictions)
    group_predictions = pd.DataFrame(
        np.array(scores), index=users_idx, columns=list_items)
    return group_predictions
