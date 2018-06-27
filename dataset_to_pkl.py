import pickle
import sys
from pprint import pprint
import numpy as np

with open('dataset/ml-1m/movies.dat',encoding='latin-1') as f:
    movie_data = f.readlines()

with open('dataset/ml-1m/ratings.dat',encoding='latin-1') as f:
    rating_data = f.readlines()

movies = {}
for movie in movie_data:
    mid,name,genres = movie.split('::')
    genres = genres.split('|')
    movies[int(mid)] = (name,genres)

num_movies,__,__ = movie_data[-1].split('::')
num_movies = int(num_movies)
num_users,__,__,__ = rating_data[-1].split('::')
num_users = int(num_users)

rating_table = np.zeros((num_movies+1,num_users+1))
print(rating_table.shape)

for rating in rating_data:
    uid,mid,rate,__ = rating.split('::')
    rating_table[int(mid),int(uid)] = rate

for i in range(1,rating_table.shape[1]):
    rating_table[0,i] = np.sum(rating_table[1:,i])/np.count_nonzero(rating_table[1:,i])
    rating_table[:,i] = rating_table[:,i] - rating_table[0,i]

with open('movie-data.pkl','wb') as f:
    pickle.dump(movies,f)

with open('ratings-data.pkl','wb') as f:
    pickle.dump(rating_table,f)   