import pickle
import numpy as np

with open('movie-data.pkl','rb') as f:
    movies = pickle.load(f)

with open('ratings-data.pkl','rb') as f:
    ratings = pickle.load(f)

def sim(mid1,mid2,ratings):
	v1 = np.array([ ratings[mid1,i]-ratings[0,i] for i in range(1,ratings.shape[0]) if ratings[mid1,i]!=0 and ratings[mid2,i]!=0])
	v2 = np.array([ ratings[mid2,i]-ratings[0,i] for i in range(1,ratings.shape[0]) if ratings[mid1,i]!=0 and ratings[mid2,i]!=0])

	if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0 or v1.shape[0] < 20:
		return 0
	else:
		return np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))

def predict(uid,mid,ratings,sim_movies):
    num = 1
    for i in range(sim_movies.shape[1]):
        num*= ratings[mid,sim_movies[mid,i]]*sim(sim_movies[mid,i])

    pred = num/abs(np.prod(sim_movies[mid]))

    return pred

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
    for i in range(1,100):
        print(f'user {user}, movie {i}')
        sim_mov = get_sim_mov(user)
        rate = predict_tmp(user,i,ratings,sim_mov)
        print(f'a: {ratings[i,user]}  pr: {rate}')
