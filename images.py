import requests
import os
from dotenv import load_dotenv

load_dotenv()

auth = os.getenv('API_AUTH')

def get_poster_image_url(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?include_image_language=en&language=en"
    headers = {
        "accept": "application/json",
        "Authorization": auth
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        posters = data.get("posters", [])
        if posters:
            # En este ejemplo, elegimos la primera imagen del póster
            poster_url = "https://image.tmdb.org/t/p/original" + posters[0]["file_path"]
            return poster_url
        else:
            return None
    else:
        print("Error al obtener la imagen del póster:", response.text)
        return None