import streamlit as st
import pandas as pd
from streamlit_card import card
from utils import ratings, movies, tags, links, svd_model, show_movie_info

st.set_page_config(layout="wide")

user_id = st.sidebar.number_input('Ingrese su ID de usuario', min_value=1, step=1)

# Obtener las 5 películas con mejor predicción para el usuario
def get_top_predicted_movies(user_id, n=12):
    predicted_ratings = []
    for movie_id in movies['movieId'].unique():
        prediction = svd_model.predict(user_id, movie_id)
        predicted_ratings.append({'movieId': movie_id, 'prediction': prediction.est})
    predicted_ratings_df = pd.DataFrame(predicted_ratings)
    top_predicted_movies = predicted_ratings_df.sort_values(by='prediction', ascending=False).head(n)
    return top_predicted_movies

# Obtener las 5 películas con mejor predicción para el usuario
top_predicted_movies = get_top_predicted_movies(user_id)

# Mostrar las 5 películas con mejor predicción para el usuario en forma de tarjetas
num_cols = 4
num_rows = (len(top_predicted_movies) - 1) // num_cols + 1
for i in range(num_rows):
    cols = st.columns(num_cols)
    for j in range(num_cols):
        index = i * num_cols + j
        if index < len(top_predicted_movies):
            movie_name, _, rating, _, poster_url = show_movie_info(user_id, top_predicted_movies.iloc[index]['movieId'])
            if movie_name:
                with cols[j]:
                    card(
                        title=movie_name,
                        text=[f"Rating: {rating}"],
                        image=poster_url,
                        styles={
                            "card": {
                                "width": "300px",
                                "height": "500px"
                            },
                            "div": {
                                "padding": "0px 0px 40px 0px"
                            }
                        }
                    )