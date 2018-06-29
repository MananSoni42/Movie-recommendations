import pickle
import numpy as np

with open('movie-data.pkl','rb') as f:
    movies = pickle.load(f)

with open('ratings-data.pkl','rb') as f:
    ratings = pickle.load(f)

with open('similar-movie-data.pkl','rb') as f:
    sim_movies = pickle.load(f)

def sim(mid1,mid2,ratings):
	v1 = ratings[mid1,1:]
	v2 = ratings[mid2,1:]
	avg = ratings[0,1:]

	ind = np.nonzero(v1*v2)

	v1_new = np.take(v1,ind) - np.take(avg,ind)
	v2_new = np.take(v2,ind) - np.take(avg,ind)

	v1 = v1_new.flatten()
	v2 = v2_new.flatten()

	if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0 or v1.shape[0] < 20:
		return 0
	else:
		return np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))

def predict_tmp(uid,mid,ratings,movies):
    num = 0
    denom = 0
    for i in range(30):
        if ratings[mid,movies[i]] == 0:
            num+= (sim(mid,movies[i],ratings)*ratings[0,movies[i]])
        else:
            num+= (sim(mid,movies[i],ratings)*ratings[mid,movies[i]])
        denom+= abs(sim(mid,movies[i],ratings))

    print(num,denom)
    return abs(num/denom)

def predict(uid,mid,ratings,sim_movies):
    num = 0
    denom = 0
    for i in range(sim_movies.shape[1]):
        if ratings[mid,sim_movies[mid,i]] == 0:
            num+= (sim(mid,sim_movies[mid,i],ratings)*ratings[0,sim_movies[mid,i]])
        else:
            num+= (sim(mid,sim_movies[mid,i],ratings)*ratings[mid,sim_movies[mid,i]])
        denom+= abs(sim(mid,sim_movies[mid,i],ratings))

    print(num,denom)
    return abs(num/denom)

def get_sim_mov(mid):
    i = mid
    k = 30
    lst = []
    for j in range(1,ratings.shape[0]):
        #print(f'{j}/{ratings.shape[0]}')
        if i!= j:
            lst.append( (j,sim(i,j,ratings)) )
    lst.sort(reverse=True,key=lambda x:x[1])
    similar = np.array([lst[l][0] for l in range(k)])
    return similar

if __name__ == '__main__':
    user = 6
    mid = 7
    print(f'user {user}, movie {mid}')
    sim_mov = get_sim_mov(mid)
    rate_2 = predict(user,mid,ratings,sim_movies)
    print(f'\na: {ratings[mid,user]}  pr: {rate_2}')
