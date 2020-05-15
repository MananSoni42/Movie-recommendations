#!/usr/bin/python3
""" A Basic command line Movie Recommendation Engine. """

import argparse
import sys
import pickle
from shutil import copyfile
import numpy as np
from movie_search import n_closest_str
from data_manip import get_data_from_pickle
from collaborative_filtering import get_n_rec

# add command line arguement parsing
parser = argparse.ArgumentParser()
parser.add_argument(
    '-s', '--search', help='Search for movies by name and rate them', action='store_true')
parser.add_argument(
    '-r', '--recommend', help='Let the system recommend movies to you', action='store_true')
parser.add_argument(
    '--reset', help='Remove all of your ratings', action='store_true')

def update_ratings(ratings, out_file='ratings-data.pkl'):
    """ Update ratings pickle file with new data. """
    with open(out_file, 'wb') as f:
        pickle.dump(ratings, f)

    copyfile(out_file,f'./backup_data/{out_file}')

def reset(ratings):
    """ Remove all user data. """
    ratings[:, 0] = 0
    update_ratings(ratings)


def search(movies):
    """ Search movie database (pickle file) for similar movies """
    user_movie = input('Enter Movie: ')

    results = n_closest_str(5, user_movie, movies)

    if results == 0:
        print('Sorry! No matches found')
        return 0

    for mid in results:
        print(f'{mid} - {movies[mid][0]}')
        print(f'genres - {movies[mid][1]}')
        print('')
    print('\n')

    num = -1
    print(results)
    while num not in results:
        try:
            num = int(input(
                'Select a movie ID from above choices to rate. (press enter only to exit): '))
        except:
            return 0

    rating = 0
    while rating not in [1, 2, 3, 4, 5]:
        try:
            rating = int(input('Rating (1-5): '))
        except:
            pass

    ratings[num, 0] = rating

    update_ratings(ratings)

    return mid, rating


def recommend(movies, ratings, similar_movies):
    """ Recommend movies to user. """
    num_rated = np.flatnonzero(ratings[:, 0]).shape[0]

    print(f'You have rated {num_rated} movies.')
    if num_rated < 5:
        print('Rate atleast 5 movies to get recommendations')
        return 0

    genres = {}
    for mid in np.flatnonzero(ratings[:, 0]):
        for genre in movies[mid][1]:
            try:
                genres[genre] += 1
            except:
                genres[genre] = 1

    results = get_n_rec(0, 5, ratings, movies, similar_movies)
    print('\nTop Recommendations:')
    for mid in results:
        print(f'{mid} - {movies[mid][0]}')
    print('')

    ind = np.flatnonzero(ratings[:, 0])
    genres = {}
    for mid in ind:
        try:
            for genre in movies[mid][1]:
                try:
                    genres[genre] += 1
                except:
                    genres[genre] = 1
        except:
            pass
    genres = sorted([(key, value) for key, value in genres.items()],
                    reverse=True, key=lambda x: x[1])[:3]

    for genre in genres:
        results = get_n_rec(0, 3, ratings, movies, similar_movies, genre[0])
        print(f'\nTop Recommendations in {genre[0]}:')
        for mid in results:
            print(f'{mid} - {movies[mid][0]}')
        print('')


if __name__ == '__main__':

    movies, ratings, similar_movies = get_data_from_pickle()
    arg = parser.parse_args()

    # display help if no arguements are given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if arg.search:
        search(movies)

    if arg.reset:
        reset(ratings)

    if arg.recommend:
        recommend(movies, ratings, similar_movies)
