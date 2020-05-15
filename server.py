from flask import Flask, render_template, request, redirect, url_for
from data_manip import get_data_from_pickle
from movie_search import n_closest_str
from shutil import copyfile
from collaborative_filtering import get_n_rec
import numpy as np
import pickle

app = Flask(__name__)
movies, ratings, similar_movies = get_data_from_pickle()

MAX_MOVIES_SEARCH = 10
MAX_RECOMMEND = 5
MAX_RECOMMEND_GENRE = 3

def update_ratings(ratings, out_file='ratings-data.pkl'):
    """ Update ratings pickle file with new data. """
    with open(out_file, 'wb') as f:
        pickle.dump(ratings, f)

    copyfile(out_file,f'./backup_data/{out_file}')

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("home.html",movies=[])
    if request.method == 'POST':
        title = request.form.get("name")
        results = n_closest_str(MAX_MOVIES_SEARCH, title, movies)
        ms = []
        if results!=0:
            for result in results:
                ms.append({
                    'id': result,
                    'title': movies[result][0],
                    'genre': ', '.join(movies[result][1])
                })
        return render_template("home.html",movies=ms)

@app.route("/recommend", methods=['GET'])
def recommend():
    err = False
    num_rated = np.flatnonzero(ratings[:, 0]).shape[0]
    ms = []
    ms_genre = []
    if num_rated < 5:
        err = True
    else:
        genres = {}
        for mid in np.flatnonzero(ratings[:, 0]):
            for genre in movies[mid][1]:
                try:
                    genres[genre] += 1
                except:
                    genres[genre] = 1

        results = get_n_rec(0, MAX_RECOMMEND, ratings, movies, similar_movies)
        for result in results:
            ms.append({
                'id': result,
                'title': movies[result][0],
                'genre': ', '.join(movies[result][1])
            })

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
            results = get_n_rec(0, MAX_RECOMMEND_GENRE, ratings, movies, similar_movies, genre[0])

            ls = []
            for result in results:
                ls.append({
                    'id': result,
                    'title': movies[result][0],
                    'genre': ', '.join(movies[result][1])
                })
            ms_genre.append({
                'genre': genre,
                'movies': ls,
            })

    return render_template("recommend.html", movies=[ms,ms_genre],err=err,num=[MAX_RECOMMEND, MAX_RECOMMEND_GENRE])

@app.route("/clear", methods=['GET'])
def clear():
    ratings[:, 0] = 0
    update_ratings(ratings)
    return redirect(url_for("index"))

@app.route("/rate", methods=['POST'])
def rate():
    id = int(request.form.get('id'))
    r = int(request.form.get('rating'))
    ratings[id, 0] = r
    update_ratings(ratings)
    return redirect(url_for("index"))

@app.route("/movies", methods=['GET'])
def get_movies():
    ms = []
    for result in np.flatnonzero(ratings[:, 0]):
        ms.append({
            'id': result,
            'title': movies[result][0],
            'genre': ', '.join(movies[result][1]),
            'rating': ratings[result,0],
        })
    return render_template('movies.html', movies=ms)

if __name__ == "__main__":
    app.run()
