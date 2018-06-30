import pickle
import numpy as np

def get_data():
    with open('movie-data.pkl','rb') as f:
        movies = pickle.load(f)
    with open('ratings-data.pkl','rb') as f:
        ratings = pickle.load(f)
    with open('similar-movie-data.pkl','rb') as f:
        sim_movies = pickle.load(f)
    return movies,ratings,sim_movies

def sim(mid1,mid2,ratings):
	v1 = ratings[mid1,1:]
	v2 = ratings[mid2,1:]
	avg = ratings[0,1:]

	ind = np.nonzero(v1*v2)

	v1_new = np.take(v1,ind) - np.take(avg,ind)
	v2_new = np.take(v2,ind) - np.take(avg,ind)

	v1 = v1_new.flatten()
	v2 = v2_new.flatten()

	if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
		return 0
	else:
		return np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))

def predict(uid,mid,ratings,sim_movies):
    num = 0
    denom = 0
    for i in range(sim_movies.shape[1]):
        if ratings[mid,sim_movies[mid,i]] == 0:
            num+= (sim(mid,sim_movies[mid,i],ratings)*ratings[0,sim_movies[mid,i]])
        else:
            num+= (sim(mid,sim_movies[mid,i],ratings)*ratings[mid,sim_movies[mid,i]])
        denom+= abs(sim(mid,sim_movies[mid,i],ratings))
    if denom == 0:
        return 0
    return round(abs(num/denom),2)

'''
#unoptimized

def get_n_rec(uid,n,ratings,movie,sim_movies,genre=None):
    if genre:
        suggestions = np.array([ predict(uid,mid,ratings,sim_movies) if ratings[mid,uid]==0 and genre in movies[mid][1] else 0 for mid in range(1,ratings.shape[0]) ])
        top_n = np.argsort(suggestions)[::-1][:n]
    else:
        suggestions = np.array([ predict(uid,mid,ratings,sim_movies) if ratings[mid,uid]==0 else 0 for mid in range(1,ratings.shape[0]) ])
        top_n = np.argsort(suggestions)[::-1][:n]
    return top_n
'''
def get_n_rec(uid,n,ratings,movie,sim_movies,genre=None):

    ind = list(np.flatnonzero(ratings[1:,uid]))
    m = 20
    if len(ind) > m:
        ind = ind[:m]

    expanded_ind = []
    for mid in ind:
        for i in range(sim_movies.shape[1]):
            expanded_ind.append(sim_movies[mid,i])

    if genre:
        print(genre)
        suggestions = [ (mid,predict(uid,mid,ratings,sim_movies)) if (ratings[mid,uid]==0 and genre in movies[mid][1]) else (mid,0) for mid in expanded_ind ]
        top_n = sorted(suggestions,reverse=True,key=lambda x:x[1])[:n]
        top_n = [t[0] for t in top_n]
    else:
        print('No genre')
        suggestions = list(set([ (mid,predict(uid,mid,ratings,sim_movies)) if ratings[mid,uid]==0 else (mid,0) for mid in expanded_ind ]))
        top_n = sorted(suggestions,reverse=True,key=lambda x:x[1])[:n]
        top_n = [t[0] for t in top_n]
    return top_n

movies,ratings,sim_movies = get_data()

print('Fetching your Recommendations...')
recommend = get_n_rec(250,5,ratings,movies,sim_movies,'Comedy')

count = 1
for mid in recommend:
    print(f'{count} - {movies[mid][0]} - {predict(250,mid,ratings,sim_movies)}')
    print(f'genre - {movies[mid][1]}\n')
    count+=1
