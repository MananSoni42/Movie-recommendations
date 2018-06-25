import pickle
import sys
from pprint import pprint

movies = {}
with open('dataset/ml-1m/movies.dat',encoding='latin-1') as f:
    data = f.readlines()

for d in data:
    movie = {}

    movie_id,movie['name'],movie['genre'] = d.split('::')
    movie['genre'] = movie['genre'].split('|')
    for i in range(len(movie['genre'])):
        movie['genre'][i] = movie['genre'][i].rstrip('\n')

    movie['genre'] = set(movie['genre'])

    movies[int(movie_id)] = movie

ratings = {}
with open('dataset/ml-1m/ratings.dat',encoding='latin-1') as f:
    data = f.readlines()

for d in data:
    uid,mid,rating,time = d.split('::')
    try:
        movies[int(mid)]['ratings'].append((int(uid),int(rating)))
    except Exception as e:
        movies[int(mid)]['ratings'] = [(int(uid),int(rating))]



#with open('movies-data.pkl','wb') as f:
#    pickle.dump(movies,f)
