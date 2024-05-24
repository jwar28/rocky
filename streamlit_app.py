import streamlit as st
from streamlit_card import card
from utils import ratings, show_movie_info
from st_pages import Page, show_pages

st.set_page_config(layout="wide", page_title="Rocky | Home")

def get_top_rated_movies(user_id, n=8):
    user_ratings = ratings[ratings['userId'] == user_id]
    top_rated_movies = user_ratings.sort_values(by='rating', ascending=False).head(n)
    return top_rated_movies

st.title('Sistema de Recomendación de Películas')

user_id = st.sidebar.number_input('Enter user id', min_value=1, step=1)

top_rated_movies = get_top_rated_movies(user_id)

st.subheader('Top rated movies by this user')

num_cols = 4
num_rows = (len(top_rated_movies) - 1) // num_cols + 1
for i in range(num_rows):
    cols = st.columns(num_cols)
    for j in range(num_cols):
        index = i * num_cols + j
        if index < len(top_rated_movies):
            movie_name, genres, rating, _, poster_url = show_movie_info(user_id, top_rated_movies.iloc[index]['movieId'])
            if movie_name:
                with cols[j]:
                    card(
                        title=movie_name,
                        text=[f"Rating: {rating}", f"{genres}"],
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
        Page("streamlit_app.py", "Top rated"),
        Page("recomendations.py", "Recommendations"),
    ]
)