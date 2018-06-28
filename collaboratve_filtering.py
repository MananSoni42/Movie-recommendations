import pickle
import numpy as np
import sys

def get_movie_data():
	with open('movie-data.pkl','rb') as f:
		movie = pickle.load(f)

	return movie

def check(i1,i2,ratings):
	count = 0
	for i in range(ratings.shape[0]):
		if ratings[i1,i] != ratings[i2,i]:
			count+=1
	print(f'diff b/w {i1} and {i2} is {count}')

def get_rating_data():
	with open('ratings-data.pkl','rb') as f:
		ratings = pickle.load(f)

	return ratings

def sim(mid1,mid2,ratings):
	v1 = np.array([ ratings[mid1,i]-ratings[0,i] for i in range(1,ratings.shape[0]) if ratings[mid1,i]!=0 and ratings[mid2,i]!=0])
	v2 = np.array([ ratings[mid2,i]-ratings[0,i] for i in range(1,ratings.shape[0]) if ratings[mid1,i]!=0 and ratings[mid2,i]!=0])

	if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0 or v1.shape[0] < 20:
		return 0
	else:
		return np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))

ratings = get_rating_data()

k = 30

similar  = np.zeros((ratings.shape[0],k))
for i in range(1,ratings.shape[0]):
	lst = []
	print(f'{i}/{ratings.shape[0]}')
	for j in range(1,ratings.shape[0]):
		if i != j:
			lst.append( (j,sim(i,j,ratings)) )
	lst.sort(reverse=True,key=lambda x:x[1])
	similar[i,:] = np.array([lst[l][0] for l in range(k)])

with open('similar-movie-data.pkl','wb') as f:
	pickle.dump(similar,f)
