import streamlit as st
import pandas as pd
from st_pages import Page, show_pages, add_page_title
import pickle
from surprise import Dataset, Reader, SVD, accuracy
from images import get_poster_image_url  # Importar la función para obtener la URL de la imagen del póster
from streamlit_card import card  # Importar la función card de streamlit_card

# Ruta de los archivos CSV
ratings_file_path = '../data/ratings.csv'
movies_file_path = '../data/movies.csv'
tags_file_path = '../data/tags.csv'
links_file_path = '../data/links.csv'
model_file_path = 'svd_model.pkl'

# Cargar datos
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
        prediction = svd_model.predict(user_id, movie_id).est
        tmdb_id = links[links['movieId'] == movie_id]['tmdbId'].values[0]
        poster_url = get_poster_image_url(tmdb_id)
        return movie_name, genres, rating, prediction, poster_url
    else:
        return None, None, None, None, None