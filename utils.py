import pandas as pd
import pickle
import requests
import io
import zipfile
from images import get_poster_image_url

url = 'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip'
r = requests.get(url)
with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    z.extractall()

ratings_file_path = 'ml-latest-small/ratings.csv'
movies_file_path = 'ml-latest-small/movies.csv'
tags_file_path = 'ml-latest-small/tags.csv'
links_file_path = 'ml-latest-small/links.csv'
model_file_path = 'svd_model.pkl'

ratings = pd.read_csv(ratings_file_path)
movies = pd.read_csv(movies_file_path)
tags = pd.read_csv(tags_file_path)
links = pd.read_csv(links_file_path)

with open(model_file_path, 'rb') as model_file:
    svd_model = pickle.load(model_file)

def show_movie_info(user_id, movie_id):
    movie_info = movies[movies['movieId'] == movie_id]
    if not movie_info.empty:
        movie_name = movie_info['title'].values[0]
        genres = movie_info['genres'].values[0]
        rating = ratings[(ratings['userId'] == user_id) & (ratings['movieId'] == movie_id)]['rating'].values
        if len(rating) > 0:
            rating = rating[0]
        else:
            rating = 'No rating available'
        prediction = round(svd_model.predict(user_id, movie_id).est, 2)
        tmdb_id = links[links['movieId'] == movie_id]['tmdbId'].values[0]
        poster_url = get_poster_image_url(tmdb_id)
        return movie_name, genres, rating, prediction, poster_url
    else:
        return None, None, None, None, None