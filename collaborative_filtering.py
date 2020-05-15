"""
Implementation of item-item collaborative filtering algorithms.

Functions:
* sim(mid1,mid2,ratings)
* predict(uid,mid,ratings,sim_movies)
* get_n_rec(uid,n,ratings,movies,sim_movies,<genre>)
"""

import pickle
import numpy as np


def sim(mid1, mid2, ratings):
    """
    Get the similarity between 2 movies

    Uses adjusted cosine similarity

    Arguements:
    mid1 (int) - id of movie 1
    mid2 (int) - id of movie 2
    ratings - rating data from pickle file.

    Returns:
    similarity between the movies(int).
    """
    v1 = ratings[mid1, :]
    v2 = ratings[mid2, :]
    avg = ratings[0, :]

    ind = np.nonzero(v1*v2)

    v1_new = np.take(v1, ind) - np.take(avg, ind)
    v2_new = np.take(v2, ind) - np.take(avg, ind)

    v1 = v1_new.flatten()
    v2 = v2_new.flatten()

    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0 or v1.shape[0] < 20:
        return 0
    else:
        return np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))


def predict(uid, mid, ratings, sim_movies):
    """
    Predict rating of a movie(mid) by a user(uid).

    Arguements:
    uid (int) - user id
    mid (int) - movie id
    ratings - rating data from pickle file
    sim_movies - similar movies data from pickle file.

    ReturnsL
    Rating (between 0 and 5)
    """
    num = 0
    denom = 0
    for i in range(sim_movies.shape[1]):
        if ratings[mid, sim_movies[mid, i]] == 0:
            num += (sim(mid, sim_movies[mid, i], ratings)
                    * ratings[0, sim_movies[mid, i]])
        else:
            num += (sim(mid, sim_movies[mid, i], ratings)
                    * ratings[mid, sim_movies[mid, i]])
        denom += abs(sim(mid, sim_movies[mid, i], ratings))
    if denom == 0:
        return 0
    return round(abs(num/denom), 2)


def get_n_rec(uid, n, ratings, movies, sim_movies, genre=None):
    """
    Get the top n movie recommendations for a user(uid).

    Arguements:
    uid (int) - user id
    n (int) - number of recommendations required
    ratings - rating data from pickle file
    movies - movie data from pickle file
    sim_movies - similar movie data from pickle file
    genre(string) - search only within specific genre
    """
    ind = list(np.flatnonzero(ratings[:, uid]))
    m = 20
    if len(ind) > m:
        ind = ind[:m]

    expanded_ind = []
    for mid in ind:
        for i in range(sim_movies.shape[1]):
            expanded_ind.append(sim_movies[mid, i])
    expanded_ind = list(set(expanded_ind))
    expanded_ind = [i for i in expanded_ind if i != 0]

    if genre:
        suggestions = [(mid, predict(uid, mid, ratings, sim_movies)) if (
            ratings[mid, uid] == 0 and genre in movies[mid][1]) else (mid, 0) for mid in expanded_ind]
        top_n = sorted(suggestions, reverse=True, key=lambda x: x[1])[:n]
        top_n = [t[0] for t in top_n]
    else:
        suggestions = list(set([(mid, predict(uid, mid, ratings, sim_movies))
                                if ratings[mid, uid] == 0 else (mid, 0) for mid in expanded_ind]))
        top_n = sorted(suggestions, reverse=True, key=lambda x: x[1])[:n]
        top_n = [t[0] for t in top_n]
    return top_n
