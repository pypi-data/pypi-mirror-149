"""Module containing helpful function for data preprocessing.

The available functions are:

.. autosummary::
    :nosignatures:

    data_cleaning
    create_train_test
    create_k_fold_cv

"""


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import random
import os


def data_cleaning(data, threshold=10, u=True, i=True, path=None, file_name="clean_data.csv"):
    """Cleans the dataset from all users or items that have very few ratings.

    Args:
        data:  Pandas Dataframe containing a user column named `uid`, an item column named `iid`, and a ratings column named `rating`.
        threshhold: The minimal ammount of ratings that the dataset should contain for each user/item.
        u: If u is False, won't clean the users. Default is True.
        i: If i is False, won't clean the items. Default is True.
        path: Path to save the cleaned data into. If not specified, the function will retrun the clean dataset.
        file_name: Name of the file where data is saved. Default is `clean_data.csv`.

    Returns:
        The cleaned dataset if `path` is not specified. Saves he results in path otherwise. 
    """
    items = np.sort(data["iid"].unique())
    users = np.sort(data["uid"].unique())
    low_items = []
    low_users = []
    clone_data = data
    if(i):  # remove all items for which there are less than 'threshold' amount of ratings
        for i in items:
            if(len(clone_data[clone_data.iid == i]) < threshold):
                low_items.append(i)
        clone_data = clone_data.drop(
            clone_data[clone_data.iid.isin(low_items)].index)

    # remove all users for which there are less than 'threshold' amount of ratings
    if(u):
        for u in users:
            if(len(clone_data[clone_data.uid == u]) < 20):
                low_users.append(u)
            clone_data = clone_data.drop(
                clone_data[clone_data.uid.isin(low_users)].index)
    return clone_data


def create_train_test(data, path, t_size=0.2):
    """Splits data into train and test sets.
    This function uses tha `scikit-learn` `train_test_split` function with a `stratify` method using users as classes.
    This way, the split keeps the same rating ratio for all users.

    Args:
        data:  Pandas Dataframe containing a user column named `uid`, an item column named `iid`, and a ratings column named `rating`.
        path: Path to save the train and test data into.
        t_size: The percentage of the test set. Default is `0.2`.


    Returns:
        Saves the train data in a `train.csv` file and the test data in the `test.csv` in specified path. 
    """
    if not os.path.exists(path):
        os.makedirs(path)
    seed = random.randint(0, 1000000)
    # train and test split :
    train, test = train_test_split(
        data, test_size=t_size, shuffle=True, stratify=data.userId, random_state=seed)

    train.to_csv(os.path.join(
        path, "train.csv"), index=False)

    test.to_csv(os.path.join(path, "test.csv"), index=False)


def create_k_fold_cv(data, path, t_size=0.2, v_size=0.25, k=5):
    """Splits data into k-fold train and validation and test sets.
    This function prepares the data for cross-validation. First splits the dataset into `train_valid` and `test` sets.
    Then splits the `train_valid` set into k-fold `train` and `valid` sets.

    Args:
        data:  Pandas Dataframe containing a user column named `uid`, an item column named `iid`, and a ratings column named `rating`.
        path: Path to save the k-fold split data into.
        t_size: The percentage of the test set. Default is `0.2`.
        v_size: The percentage of the test set. Default is `0.25`.
        k: Number of folds. Default is `5`.


    Returns:
        Saves the train_validation data in a `train_valid.csv` file and the test data in the `test.csv` in specified path. 
        Saves the folds into internal folders (ex: `fold_1`) with train set as `train.csv` and validation as set`valid.csv`.
    """
    if not os.path.exists(path):
        os.makedirs(path)
    seed = random.randint(0, 1000000)
    # train_validation and test split :
    train_valid, test = train_test_split(
        data, test_size=t_size, shuffle=True, stratify=data.userId, random_state=seed)

    train_valid.to_csv(os.path.join(path, "train_valid.csv"), index=False)

    test.to_csv(os.path.join(path, "test.csv"), index=False)

    for i in range(1, k+1):
        f_dir_name = "fold"+str(i)
        f_path = os.path.join(path, f_dir_name)
        if not os.path.exists(f_path):
            os.makedirs(f_path)

        # train and validation split:
        train, validation = train_test_split(
            train_valid, test_size=v_size, shuffle=True, stratify=train_valid.userId)

        # we save the results into files:
        train.to_csv(os.path.join(f_path, "train.csv"), index=False)

        validation.to_csv(os.path.join(f_path, "valid.csv"), index=False)
