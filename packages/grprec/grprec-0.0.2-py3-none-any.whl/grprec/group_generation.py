"""Tools for building different types of user groups from a dataset.

The available group generation methods are:

.. autosummary::
    :nosignatures:

    generate_random_group
    generate_similar_group
    generate_divergent_group
    generate_very_similar_group
    generate_very_divergent_group
    generate_greedy_similar_group
    generate_greedy_divergent_group
    read_groups
"""
import numpy as np
import pandas as pd
import random
import os


def calculate_similarities(dataset):
    """Calculates the similarities among users of the dataset using Pearson correlation. 

    Args:
        dataset: Pandas Dataframe containing a user column named `uid`, an item column named `iid`, and a ratings column named `rating`.

    Returns:
        A tuple (user_similarity_matrix, users,user_id_indexes), where user_similarity_matrix is a user*user matrix containing similarities among all users of the dataset.
        user is a list of users of the datset. user_id_indexes is a list containing indexes of user ids. 
    """

    users = set(dataset['uid'].drop_duplicates())
    user_matrix = dataset.pivot_table(
        columns="iid", index="uid", values="rating")

    user_id_indexes = user_matrix.index.values
    user_matrix = user_matrix.fillna(0)
    user_similarity_matrix = np.corrcoef(user_matrix.to_numpy())

    return user_similarity_matrix, users, user_id_indexes


def generate_random_group(users, group_size, group_num, path=None):
    """Generates groups of users by random selection. 

    Args:
        users: List of users as returned by the :meth:`calculate_similarities()` method.
        group_size: Number of users in each group.
        group_num: Number of groups to generate.
        path: Path to the folder where the results need to be saved. `None` by default.

    Returns:
        A list of the randomly generated groups if `path` is not specified. Saves the results in a file named `random_group_x` instead.
        `x` is the size of the generated groups. 
    """
    if(path == None):
        group_id = 0
        groups = []
        for i in range(0, group_num):
            group = random.sample(users, group_size)
            groups.append(group)
            group_id += 1
        return groups
    else:
        if not os.path.exists(path):
            os.makedirs(path)
        random_groups_file_name = "random_group_" + str(group_size)+".txt"
        random_groups_file_path = os.path.join(path, random_groups_file_name)
        with open(random_groups_file_path, 'w') as random_groups_file:
            for i in range(0, group_num):
                group = random.sample(users, group_size)
                group_str = '\t'.join(map(str, group))
                random_groups_file.write(group_str + '\n')


def generate_similar_group(users, group_size, group_num, user_similarity_matrix, user_id_indexes, path=None):
    """Generates groups of similar users.

    Selects one random user for each group, then builds the groups incrementally.
    From the user similarity matrix, it selects a random user that has a PCC>=0.3 with any group member.

    Args:
        users: List of users as returned by the :meth:`calculate_similarities()` method.
        group_size: Number of users in each group.
        group_num: Number of groups to generate.
        user_similarity_matrix: A matrix that contains the similarity between all users as returned by the :meth:`calculate_similarities()` method.
        user_id_indexes: A vector containing indexes of user ids as returned by the :meth:`calculate_similarities()` method.
        path: Path to the folder where the results need to be saved. `None` by default.

    Returns:
        A list of the generated similar groups if `path` is not specified. Saves the results in a file named `similar_group_x` instead.
        `x` is the size of the generated groups. 
    """
    if (path == None):
        final_groups = []
        selection = random.sample(users, group_num)
        for user in selection:
            group = [user]
            for i in range(group_size - 1):
                new_user = _select_user_for_similar_group(
                    group, user_similarity_matrix, user_id_indexes)
                if new_user is None:
                    break
                else:
                    group.extend(new_user)
            if len(group) != group_size:
                continue
            final_groups.append(group)
        return final_groups
    else:
        if not os.path.exists(path):
            os.makedirs(path)
        final_groups = []
        similar_groups_file_name = "similar_group_" + str(group_size)+".txt"
        similar_groups_file_path = os.path.join(path, similar_groups_file_name)
        with open(similar_groups_file_path, 'w') as similar_groups_file:
            selection = random.sample(users, group_num)
            for user in selection:
                group = [user]
                for i in range(group_size - 1):
                    new_user = _select_user_for_similar_group(
                        group, user_similarity_matrix, user_id_indexes)
                    if new_user is None:
                        break
                    else:
                        group.extend(new_user)
                if len(group) != group_size:
                    continue
                group_str = '\t'.join(map(str, group))
                similar_groups_file.write(group_str + '\n')


def generate_divergent_group(users, group_size, group_num, user_similarity_matrix, user_id_indexes, path=None):
    """Generates groups of divergent users.

    Selects one random user for each group, then builds the groups incrementally.
    From the user similarity matrix, it selects a random user that has a PCC<0.1 with any group member.

    Args:
        users: List of users as returned by the :meth:`calculate_similarities()` method.
        group_size: Number of users in each group.
        group_num: Number of groups to generate.
        user_similarity_matrix: A matrix that contains the similarity between all users as returned by the :meth:`calculate_similarities()` method.
        user_id_indexes: A vector containing indexes of user ids as returned by the :meth:`calculate_similarities()` method.
        path: Path to the folder where the results need to be saved. `None` by default.

    Returns:
        A list of the generated divergent groups if `path` is not specified. Saves the results in a file named `divergent_group_x` instead.
        `x` is the size of the generated groups.
    """
    if(path == None):
        final_groups = []
        selection = random.sample(users, group_num)
        for user in selection:
            group = [user]
            for i in range(group_size - 1):
                new_user = _select_user_for_divergent_group(
                    group, user_similarity_matrix, user_id_indexes)
                if new_user is None:
                    break
                else:
                    group.extend(new_user)
            if len(group) != group_size:
                continue
            final_groups.append(group)
        return final_groups
    else:
        if not os.path.exists(path):
            os.makedirs(path)
        final_groups = []
        divergent_groups_file_name = "divergent_group_" + \
            str(group_size)+".txt"
        divergent_groups_file_path = os.path.join(
            path, divergent_groups_file_name)
        with open(divergent_groups_file_path, 'w') as divergent_groups_file:
            selection = random.sample(users, group_num)
            for user in selection:
                group = [user]
                for i in range(group_size - 1):
                    new_user = _select_user_for_divergent_group(
                        group, user_similarity_matrix, user_id_indexes)
                    if new_user is None:
                        break
                    else:
                        group.extend(new_user)
                if len(group) != group_size:
                    continue
                group_str = '\t'.join(map(str, group))
                divergent_groups_file.write(group_str + '\n')


def generate_very_similar_group(users, group_size, group_num, user_similarity_matrix, user_ids_indexes, path=None):
    """Generates groups of very similar users.

    Selects one random user for each group, then builds the groups incrementally.
    From the user similarity matrix, it selects the most similar user to the group as a whole (averaged similarity).

    Args:
        users: List of users as returned by the :meth:`calculate_similarities()` method.
        group_size: Number of users in each group.
        group_num: Number of groups to generate.
        user_similarity_matrix: A matrix that contains the similarity between all users as returned by the :meth:`calculate_similarities()` method.
        user_id_indexes: A vector containing indexes of user ids as returned by the :meth:`calculate_similarities()` method.
        path: Path to the folder where the results need to be saved. `None` by default.

    Returns:
        A list of the generated very similar groups if `path` is not specified. Saves the results in a file named `very_similar_group_x` instead.
        `x` is the size of the generated groups.
    """
    if(path == None):
        final_groups = []
        selection = random.sample(users, group_num)
        for user in selection:
            group = [user]
            for i in range(group_size - 1):
                new_user = _select_user_for_very_sim_group(
                    group, user_similarity_matrix, user_ids_indexes)
                if new_user is None:
                    break
                else:
                    group.append(new_user)
            if len(group) != group_size:
                continue
            final_groups.append(group)
        return final_groups
    else:
        if not os.path.exists(path):
            os.makedirs(path)
        very_sim_groups_file_name = "very_similar_group_" + \
            str(group_size)+".txt"
        very_sim_groups_file_path = os.path.join(
            path, very_sim_groups_file_name)
        with open(very_sim_groups_file_path, 'w') as very_sim_groups_file:
            selection = random.sample(users, group_num)
            for user in selection:
                group = [user]
                for i in range(group_size - 1):
                    new_user = _select_user_for_very_sim_group(
                        group, user_similarity_matrix, user_ids_indexes)
                    if new_user is None:
                        break
                    else:
                        group.append(new_user)
                if len(group) != group_size:
                    continue
                group_str = '\t'.join(map(str, group))
                very_sim_groups_file.write(group_str + '\n')


def generate_very_divergent_group(users, group_size, group_num, user_similarity_matrix, user_ids_indexes, path=None):
    """Generates groups of very divergent users.

    Selects one random user for each group, then builds the groups incrementally.
    From the user similarity matrix, it selects the most dissimilar user to the group as a whole (averaged similarity).

    Args:
        users: List of users as returned by the :meth:`calculate_similarities()` method.
        group_size: Number of users in each group.
        group_num: Number of groups to generate.
        user_similarity_matrix: A matrix that contains the similarity between all users as returned by the :meth:`calculate_similarities()` method.
        user_id_indexes: A vector containing indexes of user ids as returned by the :meth:`calculate_similarities()` method.
        path: Path to the folder where the results need to be saved. `None` by default.

    Returns:
        A list of the generated very divergent groups if `path` is not specified. Saves the results in a file named `very_divergent_group_x` instead.
        `x` is the size of the generated groups.
    """
    if(path == None):
        final_groups = []
        selection = random.sample(users, group_num)
        for user in selection:
            group = [user]
            for i in range(group_size - 1):
                new_user = _select_user_for_very_div_group(
                    group, user_similarity_matrix, user_ids_indexes)
                if new_user is None:
                    break
                else:
                    group.append(new_user)
            if len(group) != group_size:
                continue
            final_groups.append(group)
        return final_groups
    else:
        if not os.path.exists(path):
            os.makedirs(path)
        very_div_groups_file_name = "very_divergent_group_" + \
            str(group_size)+".txt"
        very_div_groups_file_path = os.path.join(
            path, very_div_groups_file_name)
        with open(very_div_groups_file_path, 'w') as very_div_groups_file:
            selection = random.sample(users, group_num)
            for user in selection:
                group = [user]
                for i in range(group_size - 1):
                    new_user = _select_user_for_very_div_group(
                        group, user_similarity_matrix, user_ids_indexes)
                    if new_user is None:
                        break
                    else:
                        group.append(new_user)
                if len(group) != group_size:
                    continue
                group_str = '\t'.join(map(str, group))
                very_div_groups_file.write(group_str + '\n')


def generate_greedy_similar_group(users, group_size, group_num, user_similarity_matrix, user_ids_indexes, path=None):
    """Generates groups of similar users using a 'Greedy' approach.

    Selects one random user for each group. Then, from the user similarity matrix, it selects the most similar 
    users to the first selected user.

    Args:
        users: List of users as returned by the :meth:`calculate_similarities()` method.
        group_size: Number of users in each group.
        group_num: Number of groups to generate.
        user_similarity_matrix: A matrix that contains the similarity between all users as returned by the :meth:`calculate_similarities()` method.
        user_id_indexes: A vector containing indexes of user ids as returned by the :meth:`calculate_similarities()` method.
        path: Path to the folder where the results need to be saved. `None` by default.

    Returns:
        A list of the generated greedy similar groups if `path` is not specified. Saves the results in a file named `greedy_similar_group_x` instead.
        `x` is the size of the generated groups.
    """

    if(path == None):
        final_groups = []
        selection = random.sample(users, group_num)
        for user in selection:
            group = [user]
            new_users = _select_greedy_similars_for_user(
                user, group_size-1, user_similarity_matrix, user_ids_indexes)
            for u in new_users:
                group.append(u)
            final_groups.append(group)
        return final_groups
    else:
        if not os.path.exists(path):
            os.makedirs(path)
        greedy_sim_groups_file_name = "greedy_similar_group_" + \
            str(group_size)+".txt"
        greedy_sim_groups_file_path = os.path.join(
            path, greedy_sim_groups_file_name)
        with open(greedy_sim_groups_file_path, 'w') as greedy_sim_groups_file:
            selection = random.sample(users, group_num)
            for user in selection:
                group = [user]
                new_users = _select_greedy_similars_for_user(
                    user, group_size-1, user_similarity_matrix, user_ids_indexes)
                for u in new_users:
                    group.append(u)
                group_str = '\t'.join(map(str, group))
                greedy_sim_groups_file.write(group_str + '\n')


def generate_greedy_divergent_group(users, group_size, group_num, user_similarity_matrix, user_ids_indexes, path=None):
    """Generates groups of divergent users using a 'Greedy' approach.

    Selects one random user for each group. Then, from the user similarity matrix, it selects the most dissimilar 
    users to the first selected user.

    Args:
        users: List of users as returned by the :meth:`calculate_similarities()` method.
        group_size: Number of users in each group.
        group_num: Number of groups to generate.
        user_similarity_matrix: A matrix that contains the similarity between all users as returned by the :meth:`calculate_similarities()` method.
        user_id_indexes: A vector containing indexes of user ids as returned by the :meth:`calculate_similarities()` method.
        path: Path to the folder where the results need to be saved. `None` by default.

    Returns:
        A list of the generated greedy divergent groups if `path` is not specified. Saves the results in a file named `greedy_divergent_group_x` instead.
        `x` is the size of the generated groups. 
    """
    if(path == None):
        final_groups = []
        selection = random.sample(users, group_num)
        for user in selection:
            group = [user]
            new_users = _select_greedy_divergents_for_user(
                user, group_size-1, user_similarity_matrix, user_ids_indexes)
            for u in new_users:
                group.append(u)
            final_groups.append(group)
        return final_groups
    else:
        if not os.path.exists(path):
            os.makedirs(path)
        greedy_div_groups_file_name = "greedy_divergent_group_" + \
            str(group_size)+".txt"
        greedy_div_groups_file_path = os.path.join(
            path, greedy_div_groups_file_name)
        with open(greedy_div_groups_file_path, 'w') as greedy_div_groups_file:
            selection = random.sample(users, group_num)
            for user in selection:
                group = [user]
                new_users = _select_greedy_divergents_for_user(
                    user, group_size-1, user_similarity_matrix, user_ids_indexes)
                for u in new_users:
                    group.append(u)
                group_str = '\t'.join(map(str, group))
                greedy_div_groups_file.write(group_str + '\n')


def read_groups(path):
    """Reads thr groups saved in files generated by the `group_generation` module.

    Args:
        path: Path to the groups file.

    Returns:
        A list of groups read from the file.
    """
    groups = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n').split('\t')
            groups.append(line)
    return groups


def _select_user_for_similar_group(group, sim_matrix, user_id_indexes):

    for u in group:
        indexes = np.where(sim_matrix[u-1] >= 0.3)[0].tolist()
        user_ids = [user_id_indexes[index] for index in indexes]
        ids_to_select_from = set(user_ids)
    candidate_ids = ids_to_select_from.difference(set(group))
    if len(candidate_ids) == 0:
        return None
    else:
        selection = random.sample(candidate_ids, 1)
        return selection


def _select_user_for_divergent_group(group, sim_matrix, user_id_indexes):

    for u in group:
        indexes = np.where(sim_matrix[u-1] < 0.1)[0].tolist()
        user_ids = [user_id_indexes[index] for index in indexes]
        ids_to_select_from = set(user_ids)
    candidate_ids = ids_to_select_from.difference(set(group))
    if len(candidate_ids) == 0:
        return None
    else:
        selection = random.sample(candidate_ids, 1)
        return selection


def _average_sim_for_group(group, sim_matrix):
    avg_sim_vector = []
    for i in range(len(sim_matrix)):
        cumulative = 0
        for u in group:
            cumulative = cumulative + sim_matrix[u-1][i]
        avg_sim_vector.append(cumulative/len(group))
    return avg_sim_vector


def _select_user_for_very_sim_group(group, sim_matrix, user_id_indexes):
    member_similarities = np.array(_average_sim_for_group(group, sim_matrix))
    indexes = member_similarities.argsort()[::-1].tolist()
    user_ids = [user_id_indexes[index] for index in indexes]
    for member in user_ids:
        if member not in group:
            return member.tolist()


def _select_user_for_very_div_group(group, sim_matrix, user_id_indexes):
    member_similarities = np.array(_average_sim_for_group(group, sim_matrix))
    indexes = member_similarities.argsort().tolist()
    user_ids = [user_id_indexes[index] for index in indexes]
    for member in user_ids:
        if member not in group:
            return member.tolist()


def _select_greedy_similars_for_user(user, num_members, sim_matrix, user_id_indexes):
    user_vector = np.array(sim_matrix[user-1])
    indexes = user_vector.argsort()[::-1].tolist()
    user_ids = [user_id_indexes[index] for index in indexes]

    return user_ids[1:num_members+1]


def _select_greedy_divergents_for_user(user, num_members, sim_matrix, user_id_indexes):
    user_vector = np.array(sim_matrix[user-1])
    indexes = user_vector.argsort().tolist()
    user_ids = [user_id_indexes[index] for index in indexes]

    return user_ids[0:num_members]
