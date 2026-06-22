from movie_storage_sql import list_movies

STAR_URL = "https://www.citypng.com/public/uploads/preview/download-star-silhouette-orange-icon-png-735811696934096ugpfr7gzzd.png"

def read_html_file(file_path):
    """ Reads an HTML file """
    with open(file_path, "r") as handle:
        return handle.read()


def serialize_single_movie(movie_info):
    """ Serializes following information about each movie if existing:\n
        - title
        - year
        - rating
        - poster_url """
    movie_info_str = f'<li><div class="movie"><div class="movie-rating">{movie_info["rating"]}<img class=star-icon src= "{STAR_URL}"/></div>'
    if "poster_url" in movie_info.keys():
        image = f'<img class="movie-poster" src="{movie_info["poster_url"]}"/>'
        movie_info_str += image
    movie_info_str += f'<div class="movie-title">{movie_info["title"]}</div><div class="movie-year">{movie_info["year"]}</div></div>'
    return movie_info_str


def get_all_movies_info_as_string():
    """ Serializes following information about each movie if existing to html:\n
        - title
        - year
        - rating
        - poster_url """
    movies_info = list_movies()
    if not movies_info:
        return "<h2>Couldn't find any movies in your database.</h2>"
    movies_info_string = ''
    for movie_info in movies_info:
        movies_info_string += serialize_single_movie(movie_info)
    return movies_info_string


def generate_html_file():
    html_template = read_html_file("movies_template.html")
    movies_info = get_all_movies_info_as_string()
    html_output = html_template.replace("__REPLACE_MOVIE_INFO__", movies_info)
    with open("movies.html", "w") as handle:
        handle.write(html_output)
    print("\x1b[0mWebsite was generated successfully.\x1b[0m")




