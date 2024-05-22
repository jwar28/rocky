import streamlit as st
from st_pages import Page, show_pages
from streamlit_card import card
from utils import ratings, movies, tags, links, svd_model, show_movie_info

st.set_page_config(layout="wide")

# Obtener las 10 películas mejor calificadas por el usuario
def get_top_rated_movies(user_id, n=8):
    user_ratings = ratings[ratings['userId'] == user_id]
    top_rated_movies = user_ratings.sort_values(by='rating', ascending=False).head(n)
    return top_rated_movies

# Interfaz de Streamlit
st.title('Sistema de Recomendación de Películas')

# Solicitar ID de usuario en la barra lateral
user_id = st.sidebar.number_input('Ingrese su ID de usuario', min_value=1, step=1)

# Obtener las 10 películas mejor calificadas por el usuario
top_rated_movies = get_top_rated_movies(user_id)

st.subheader('Top Películas Mejor Calificadas por el Usuario')

# Mostrar las 10 películas mejor calificadas por el usuario en forma de tarjetas
num_cols = 4
num_rows = (len(top_rated_movies) - 1) // num_cols + 1
for i in range(num_rows):
    cols = st.columns(num_cols)
    for j in range(num_cols):
        index = i * num_cols + j
        if index < len(top_rated_movies):
            movie_name, _, rating, _, poster_url = show_movie_info(user_id, top_rated_movies.iloc[index]['movieId'])
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

show_pages(
    [
        Page("streamlit_app.py", "Home"),
        Page("recomendations.py", "Recomendaciones"),
    ]
)