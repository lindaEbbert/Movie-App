import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_all_movie_infos_by_title(title):
    """ Gets movie info (title, year, rating, poster_url) by title
    :param title: title of the movie
    :return: dictionary containing the movie info
    """
    response = requests.get(f"https://www.omdbapi.com/?apikey={API_KEY}&t={title}")
    response_json = response.json()
    results = {"title": response_json["Title"],
               "year": response_json["Year"],
               "rating": response_json["imdbRating"],
               "poster_url": response_json["Poster"]}
    return results

