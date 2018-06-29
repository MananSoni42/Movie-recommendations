import pickle
from difflib import SequenceMatcher
import re

with open('movie-data.pkl','rb') as f:
    movies = pickle.load(f)

user_movie = input('Enter a Movie: ').lower().strip(' ')

get_movie = lambda mid: re.sub(r'\(\d+\)','',movies[mid][0]).strip(' ').lower()

def get_similarity(s1,s2):
    t0 = sorted(list(set(s1.split(' ')).intersection(set(s2.split(' ')))))
    t1 = sorted(list(set(t0 + s1.split(' '))))
    t2 = sorted(list(set(t0 + s2.split(' '))))

    r01 = SequenceMatcher(None, t0, t1).ratio()
    r02 = SequenceMatcher(None, t0, t2).ratio()
    r12 = SequenceMatcher(None, t1, t2).ratio()
    return max(r01,r02,r12)

def n_closest_str(n,user_movie,movies):
    sim = {}
    for i in movies.keys():
        sim[i] = get_similarity(user_movie,get_movie(i))

    lst = [ (key,value) for key,value in sim.items() ]
    lst = sorted(lst,reverse=True,key=lambda x:x[1])

    print('')

    if lst[0][1] == 0:
        print('Sorry! No matches Found')
        return 0

    for i,j in lst[:n]:
        if j!=0:
            print(f'{i} - {movies[i][0]}')
            print(f'genres: {movies[i][1]}')
            print('')

n_closest_str(5,user_movie,movies)
