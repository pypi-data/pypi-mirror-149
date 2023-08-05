"""Diffrent metrics used to evaluate group recommendations.

The available metrics are:

.. autosummary::
    :nosignatures:

    precision_k
    recall
    average_precision_k
    dfh_k
    ndcg_k
    ndcg_k2

"""

import math


def precision_k(lst, ground_truth, k):
    """Calculates the precision between a recommended list of items and a ground truth at the `k` position. 

    .. math::
        \\text{precision@k(g/u)}= \\frac{ | predicted_k(g/u) \\cap relevant(g/u) | }{k}.

    Args:
        lst: List of top recommended items.
        ground_truth: List of the ground truth items.
        k: Position.

    Returns:
        The precision at the `k`th position. 
    """
    if len(lst) > k:
        lst = lst[:k]

    return ((len(set(lst) & set(ground_truth)))/len(lst))


def _relk(list, ground_truth, k):
    if list[k-1] in ground_truth:
        return 1
    else:
        return 0


def average_precision_k(list, ground_truth):
    """Calculates the average precision between a recommended list of items and a ground truth. 

    .. math::
        \\text{average_precision@k(g/u)}= \\frac{\\displaystyle \\sum_{k}precision@k(g/u)*rel(k)}{|relevant(g/u)|}.

    where: 

    .. math::
        \\text{rel(k)}= \\begin{cases} 1 & \\text{ if } predicted[k]\in \\text{relevant(g/u)} \\\ 0 & \\text{ otherwise} \\end{cases}

    Args:
        lst: List of top recommended items.
        ground_truth: List of the ground truth items.

    Returns:
        The average precision.
    """

    score = 0.0
    for i in range(1, len(list)):
        score += precision_k(list, ground_truth, i) * \
            _relk(list, ground_truth, i)
    return score/len(ground_truth)


def _dcgk(list, ground_truth, k):

    if len(list) > k:
        list = list[:k+1]
    dcg = 0.0
    for i in range(k):
        if list[i] in ground_truth:
            dcg += 1 / math.log2(i+2)
    return dcg


def ndcg_k(list, ground_truth, k):
    """Calculates the Normalized Discounted Cumulative Gain between a recommended list of items and a ground truth at the `k` position by using Binary Relevance. 

    .. math::
        \\text{nDCG@k(g/u)}= \\frac{DCG@k(g/u)}{iDCG@k(g/u)}.
    where:

    .. math::
        \\text{DCG@k(g/u)}= \\displaystyle \\sum_{j=1}^k \\frac{2^{relevance(i_j,g/u)}-1}{log_2(1+j)} .
    and:

    .. math::
        \\text{iDCG@k(g/u)}= \\displaystyle \\sum_{j=1}^k \\frac{1}{log_2(1+j)}.

    This metric uses binary relevance which is defined by:

    .. math::
        relevance(i,g/u)=\\begin{cases} 1 & \\text{ if } i\in \\text{relevant(g/u)} \\\ 0 & \\text{ otherwise} \\end{cases}.

    Args:
        lst: List of top recommended items.
        ground_truth: List of the ground truth items.

    Returns:
        The Normalized Discounted Cumulative Gain at the `k` position. 
    """
    dcg_max = 0.0
    for i in range(1, k+1):
        dcg_max += 1 / math.log2(i+1)
    return _dcgk(list, ground_truth, k) / dcg_max


def dfh_k(list, ground_truth):
    """Calculates the Discounted First Hit between a recommended list of items and a ground truth. 

    .. math::
        \\text{dfh@k(g/u)}= \\frac{1}{\\log_2(fhr+1)}.

    where `fhr` is the rank of the first hit in the recommended list of items.    

    Args:
        lst: List of top recommended items.
        ground_truth: List of the ground truth items.

    Returns:
        The Discounted First Hit. 
    """
    for i in range(len(list)):
        if list[i] in ground_truth:
            fhr = i+1
            return 1/math.log2(fhr+1)
    return 0


def recall(lst, ground_truth):
    """Calculates the recall between a recommended list of items and a ground truth. 

    .. math::
        \\text{recall@k(g/u)}= \\frac{ |predicted_k(g/u) \\cap relevant(g/u) | }{relevant(g/u)}.

    Args:
        lst: List of top recommended items.
        ground_truth: List of the ground truth items.

    Returns:
        The recall at the `k`th position. 
    """

    if (len(ground_truth) == 0):
        return 0.0

    return ((len(set(lst) & set(ground_truth)))/len(ground_truth))


def _dcgk2(list, ground_truth, k):
    dcg = 0.0
    for i in range(k):
        if list[i] in ground_truth:
            dcg += ground_truth[list[i]][0] / math.log2(i+2)
    return dcg


def ndcg_k2(list, ground_truth, k):
    dcg_max = 0.0
    for i in range(0, min(k, len(ground_truth))):
        dcg_max += ground_truth.iloc[0, i] / math.log2(i+2)
    return _dcgk2(list, ground_truth, k) / dcg_max
