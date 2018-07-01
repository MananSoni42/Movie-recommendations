""" Basic string matcher for Searching movies. """

import pickle
from difflib import SequenceMatcher
import re


def get_similarity(s1, s2):
    """ Measure of how similar str s1 and s2 are. """
    t0 = sorted(list(set(s1.split(' ')).intersection(set(s2.split(' ')))))
    t1 = sorted(list(set(t0 + s1.split(' '))))
    t2 = sorted(list(set(t0 + s2.split(' '))))

    r01 = SequenceMatcher(None, t0, t1).ratio()
    r02 = SequenceMatcher(None, t0, t2).ratio()
    r12 = SequenceMatcher(None, t1, t2).ratio()
    return max(r01, r02, r12)


def n_closest_str(n, user_movie, movies):
    """ Give the n most similar movies to the user string from the movie database. """

    def get_movie(mid): return re.sub(
        r'\(\d+\)', '', movies[mid][0]).strip(' ').lower()

    sim = {}
    for i in movies.keys():
        sim[i] = get_similarity(user_movie, get_movie(i))

    lst = [(key, value) for key, value in sim.items()]
    lst = sorted(lst, reverse=True, key=lambda x: x[1])

    print('')

    if lst[0][1] == 0:
        return 0

    lst = [i[0] for i in lst]

    return lst[:n]
