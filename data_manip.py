"""
Helps to load dataset to pickle files or to load pickle files in python.

Functions:
* get_pickle_from_dataset()
    * generate_movies()
    * generate_ratings(movies)
    * generate_similar_movies(k,ratings)
* get_data_from_pickle().
"""

import pickle
import numpy as np
from shutil import copyfile
from collaborative_filtering import sim
import os
from tqdm import tqdm

if not os.path.exists('./backup_data'):
    os.makedirs('./backup_data')


def generate_movies(out_file='movie-data.pkl'):
    """
    Generate a pickle files containing details about each movie.

    Format of pickle file:
        dictionary with
            key: movie-id (int)
            value: (Name,[genres]) - (string,list).

    Arguements:
    out_file (optional) (default: movie-data.pkl) - name of pickle file to store data.

    Returns:
    generated data as a dictionary.
    """

    # open dataset
    with open('dataset/ml-1m/movies.dat', encoding='latin-1') as f:
        movie_data = f.readlines()

    # generate pickle file
    movies = {}
    for movie in movie_data:
        mid, name, genres = movie.split('::')
        genres = genres.split('|')
        for i in range(len(genres)):
            genres[i] = genres[i].rstrip('\n')
        movies[int(mid)] = (name, genres)

    print(f'writing to {out_file}')
    # save top pickle file
    with open(out_file, 'wb') as f:
        pickle.dump(movies, f)

    # save a copy to backup_data/
    copyfile(out_file, f'./backup_data/{out_file}')
    print('Done\n')

    return movies


def generate_ratings(movies, out_file='ratings-data.pkl'):
    """
    Generate a pickle files containing details about ratiings of users with movies.

    Format of pickle file:
        numpy array (ratings) of size (num_movies+1,num_users+1)
        ratings[:,0] -> current user
        ratings[0,:] -> average user ratings of all movies
        movie id start with 1, index 0 stores user averages across all movies.

    Arguements:
    movies - dictionary in the format of { movie_id: (name,[list,of,genres]) }
    out_file (optional) (default: ratings-data.pkl) - name of pickle file to store data.

    Returns:
    generated data as a numpy array.

    """

    # open dataset
    with open('dataset/ml-1m/movies.dat', encoding='latin-1') as f:
        movie_data = f.readlines()
    with open('dataset/ml-1m/ratings.dat', encoding='latin-1') as f:
        rating_data = f.readlines()

    # generate ratings
    num_movies, __, __ = movie_data[-1].split('::')
    num_movies = int(num_movies)
    num_users, __, __, __ = rating_data[-1].split('::')
    num_users = int(num_users)

    rating_table = np.zeros((num_movies+1, num_users+1))

    for rating in rating_data:
        uid, mid, rate, __ = rating.split('::')
        rating_table[int(mid), int(uid)] = rate

    for i in range(1, rating_table.shape[1]):
        rating_table[0, i] = round(
            np.sum(rating_table[1:, i])/np.count_nonzero(rating_table[1:, i]), 3)

    # save to pickle file
    print(f'writing to {out_file}')
    with open(out_file, 'wb') as f:
        pickle.dump(rating_table, f)

    # save a copy to backup_data/
    copyfile(out_file, f'./backup_data/{out_file}')
    print('Done\n')

    return rating_table


def generate_similar_movies(ratings, k=30, out_file='similar-movie-data.pkl'):
    """
    Generate pickle file with data for similar movies.

    Creates a numpy array storing thr k most similar movies corresponding
    to each movie.

    Requires sim() function from collaborative_filtering.py.

    Format of pickle file:
        numpy array of (size num_movies+1,k).

    Arguements:
    k (int) (optional) (default: 30) - number of similar movies to store per movie
    ratings - numpy array of size (num_movies+1,num_users+1) corresponding to user ratings
    out_file (optional) (default: similar-movie-data.pkl) - name of pickle file to store data.

    Returns:
    generated data as a numpy array.
    """

    similar = np.zeros((ratings.shape[0], k))

    # generate numpy array with top k similar movies for each movie
    for i in tqdm(range(1,ratings.shape[0])):
        lst = []
        for j in range(1, ratings.shape[0]):
            if i != j:
                lst.append((j, sim(i, j, ratings)))
        lst.sort(reverse=True, key=lambda x: x[1])
        similar[i] = np.array([lst[l][0] for l in range(k)])

    similar = np.array(similar, dtype='int')

    # save to a pickle file
    print(f'writing to {out_file}')
    with open(out_file, 'wb') as f:
        pickle.dump(similar, f)

    # save a copy to backup_data/
    copyfile(out_file, f'./backup_data/{out_file}')
    print('Done')
    return similar


def get_pickle_from_dataset():
    """ Wrapper to generate all data from dataset"""
    movies = generate_movies()
    ratings = generate_ratings(movies)
    generate_similar_movies(ratings)


def get_data_from_pickle():
    """
    Get data from pickle files.

    Returns:
    ratings,movie,similar_movies if Data is found
    False otherwise
    """
    try:
        with open('movie-data.pkl', 'rb') as f:
            movie = pickle.load(f)
        with open('ratings-data.pkl', 'rb') as f:
            ratings = pickle.load(f)
        with open('similar-movie-data.pkl', 'rb') as f:
            similar = pickle.load(f)
        return movie, ratings, similar
    except:
        with open('backup_data/movie-data.pkl', 'rb') as f:
            movie = pickle.load(f)
        with open('backup_data/ratings-data.pkl', 'rb') as f:
            ratings = pickle.load(f)
        with open('backup_data/similar-movie-data.pkl', 'rb') as f:
            similar = pickle.load(f)
        return movie, ratings, similar
    else:
        return False


if __name__ == '__main__':
    movies = generate_movies()
    ratings = generate_ratings(movies)
    generate_similar_movies(ratings)
