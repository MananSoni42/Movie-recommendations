import pickle
import numpy as np

def get_movie_data():
	with open('movie-data.pkl','rb') as f:
		movie = pickle.load(f)

	return movie	

def get_rating_data():
	with open('ratings-data.pkl','rb') as f:
		ratings = pickle.load(f)	

	return ratings

def sim(mid1,mid2,ratings):
	v1 = ratings[mid1,1:]
	v2 = ratings[mid2,1:] 

	return abs(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))
	
ratings = get_rating_data()

k = 5

similar  = np.zeros((ratings.shape[0],k))

for i in range(1,ratings.shape[0]):
	print(f'{i}/{ratings.shape[0]}')
	lst = []
	for j in range(1,ratings.shape[0]):	
		if i != j:	
			lst.append( (j,sim(i,j,ratings)) )
	lst.sort(reverse=True,key=lambda x:x[1])
	similar[i,:] = np.array([lst[l][0] for l in range(k)])

with open('similar-movie-data.pkl','wb') as f:
	pickle.dump(similar,f)