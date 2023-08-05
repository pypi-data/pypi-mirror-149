"""This module contains several group score aggregation strategies in litterature.

The available strategies are:

.. autosummary::
    :nosignatures:

    AVG
    LMS
    MPL
    MUL
    AVM
    APP
    MRP
"""
import pandas as pd
import numpy as np


def AVG(group_scores_matrix, list_items):
    """Average strategy.
    Aggregates the individual scores of a group into group score by calculating the average.

    Args:
        group_scores_matrix: A dataframe containing the predicted scores for every item in the dataset by the group members.
        list_items: List of items to which the aggregation is applied to.

    Returns:
        Dataframe containing the aggregated scores using `Average` for the group and the listed items sorted from highest rated to lowest.
    """
    group = group_scores_matrix.index.tolist()
    agregated_scores = []
    for i in list_items:
        s = 0
        for u in group:
            s = s+group_scores_matrix[i][str(u)]
        s = s/len(group)
        agregated_scores.append(s)
    agregated_scores_df = pd.DataFrame(
        np.array(agregated_scores), index=list_items, columns=["group_scores"])
    return agregated_scores_df.sort_values(by=["group_scores"], ascending=False)[:20].transpose()


def LMS(group_scores_matrix, list_items):
    """Least Misery strategy.
    Aggregates the individual scores of a group into group score by selecting the minimum rating.

    Args:
        group_scores_matrix: A dataframe containing the predicted scores for every item in the dataset by the group members.
        list_items: List of items to which the aggregation is applied to.

    Returns:
        Dataframe containing the aggregated scores using `Least Misery` for the group and the listed items sorted from highest rated to lowest.
    """
    agregated_scores = []
    for i in list_items:
        s = min(group_scores_matrix[i])
        agregated_scores.append(s)
    agregated_scores_df = pd.DataFrame(
        np.array(agregated_scores), index=list_items, columns=["group_scores"])
    return agregated_scores_df.sort_values(by=["group_scores"], ascending=False)[:20].transpose()


def MPL(group_scores_matrix, list_items):
    """Most Pleasure strategy.
    Aggregates the individual scores of a group into group score by selecting the maximum rating.

    Args:
        group_scores_matrix: A dataframe containing the predicted scores for every item in the dataset by the group members.
        list_items: List of items to which the aggregation is applied to.

    Returns:
        Dataframe containing the aggregated scores using `Most Pleasure` for the group and the listed items sorted from highest rated to lowest.
    """
    agregated_scores = []
    for i in list_items:
        s = max(group_scores_matrix[i])
        agregated_scores.append(s)
    agregated_scores_df = pd.DataFrame(
        np.array(agregated_scores), index=list_items, columns=["group_scores"])
    return agregated_scores_df.sort_values(by=["group_scores"], ascending=False)[:20].transpose()


def MUL(group_scores_matrix, list_items):
    """Multiplicative strategy.
    Aggregates the individual scores of a group into group score by multiplying the individual scores.

    Args:
        group_scores_matrix: A dataframe containing the predicted scores for every item in the dataset by the group members.
        list_items: List of items to which the aggregation is applied to.

    Returns:
        Dataframe containing the aggregated scores using `Multiplicative` for the group and the listed items sorted from highest rated to lowest.
    """
    group = group_scores_matrix.index.tolist()
    agregated_scores = []
    for i in list_items:
        s = 1
        for u in group:
            s = s*group_scores_matrix[i][str(u)]
        agregated_scores.append(s)
    agregated_scores_df = pd.DataFrame(
        np.array(agregated_scores), index=list_items, columns=["group_scores"])
    return agregated_scores_df.sort_values(by=["group_scores"], ascending=False)[:20].transpose()


def AVM(group_scores_matrix, list_items, threshold):
    """Average Without Misery strategy.
    Aggregates the individual scores of a group into group score by removing items that score below a certain threthold for at least one user, Then calculating the average of the remaining items.

    Args:
        group_scores_matrix: A dataframe containing the predicted scores for every item in the dataset by the group members.
        list_items: List of items to which the aggregation is applied to.
        threshold: Select only items that score above this threshold for all members.

    Returns:
        Dataframe containing the aggregated scores using `Average Without Misery` for the group and the listed items sorted from highest rated to lowest.
    """
    group = group_scores_matrix.index.tolist()
    agregated_scores = []
    items_above_threshold = []
    for i in list_items:
        if (not (group_scores_matrix[i] < threshold).any()):
            s = 0
            items_above_threshold.append(i)
            for u in group:
                s = s+group_scores_matrix[i][str(u)]
            s = s/len(group)
            agregated_scores.append(s)
    agregated_scores_df = pd.DataFrame(np.array(
        agregated_scores), index=items_above_threshold, columns=["group_scores"])
    return agregated_scores_df.sort_values(by=["group_scores"], ascending=False)[:20].transpose()


def APP(group_scores_matrix, list_items, threshold):
    """Approval Voting strategy.
    Aggregates the individual scores of a group into group score by counting each time the items score above a certain threshold.

    Args:
        group_scores_matrix: A dataframe containing the predicted scores for every item in the dataset by the group members.
        list_items: List of items to which the aggregation is applied to.
        threshold: Count how many times each item score above this threshold

    Returns:
        Dataframe containing the aggregated scores using `Approval Voting` for the group and the listed items sorted from highest rated to lowest.
    """
    agregated_scores = []
    for i in list_items:
        s = np.sum(group_scores_matrix[i] >= threshold)
        agregated_scores.append(s)
    agregated_scores_df = pd.DataFrame(
        np.array(agregated_scores), index=list_items, columns=["group_scores"])
    return agregated_scores_df.sort_values(by=["group_scores"], ascending=False)[:20].transpose()


def MRP(group_scores_matrix, list_items, dictator):
    """Most Respected Person strategy.
    Aggregates the individual scores of a group into group score by selecting the scores of the `Most Respected Person` amongs members. (Dictatorship)

    Args:
        group_scores_matrix: A dataframe containing the predicted scores for every item in the dataset by the group members.
        list_items: List of items to which the aggregation is applied to.
        dictator: The user who's considered the `Most Respected`

    Returns:
        Dataframe containing the aggregated scores using `Most Respected Person` for the group and the listed items sorted from highest rated to lowest.
    """
    group = group_scores_matrix.index.tolist()
    if dictator in group:
        agregated_scores = group_scores_matrix.loc[dictator]
        agregated_scores_df = pd.DataFrame(
            np.array(agregated_scores), index=list_items, columns=["group_scores"])
        return agregated_scores_df.sort_values(by=["group_scores"], ascending=False)[:20].transpose()
