# Movie-App

A command-line application for managing your personal movie database. Add movies by title, and the app automatically fetches their release year, IMDb rating, and poster from the [OMDb API](https://www.omdbapi.com/). You can browse, search, sort, filter, and analyze your collection, and even generate a styled HTML website to showcase it.

## About the Project

Keeping track of the movies you've watched or want to watch can quickly become messy. **Movie-App** solves this by storing your movies in a local SQLite database and enriching each entry with data pulled from the OMDb API, so you only ever need to type a title.

The app is built around a simple text menu and offers statistics, a random movie picker, a rating histogram, and an automatically generated, good-looking website for your collection.

**Target audience:** movie enthusiasts who want a lightweight, self-hosted way to organize their film collection, and Python learners interested in a practical project that combines a database, a REST API, and HTML generation.

## Features

- **List** all movies with title, year, and rating
- **Add** a movie by title (year, rating, and poster are fetched automatically from OMDb)
- **Delete** and **update** existing movies
- **Statistics** — average rating, median rating, and best/worst movies
- **Random** movie suggestion for tonight
- **Search** by partial title, with fuzzy "did you mean?" suggestions
- **Sort** movies by rating or by year
- **Filter** movies by minimum rating and release-year range
- **Histogram** of all ratings, saved as a PNG image
- **Website generation** — export your collection to a styled `movies.html` page

## Tech Stack

- **Python 3**
- **SQLite** via [SQLAlchemy](https://www.sqlalchemy.org/) for storage
- **[OMDb API](https://www.omdbapi.com/)** for movie data
- **requests** for API calls
- **fuzzywuzzy** / **python-Levenshtein** for fuzzy search
- **matplotlib** for the ratings histogram

## Getting Started

### Prerequisites

- Python 3.10 or newer
- A free OMDb API key — request one at [omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lindaEbbert/Movie-App.git
   cd Movie-App
   ```

2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OMDb API key:
   ```env
   API_KEY=your_api_key_here
   ```

## Usage

Run the application from the project root:

```bash
python main.py
```

You'll be greeted with a menu of options:

```
Menu:
0.  Exit
1.  List movies
2.  Add movie
3.  Delete movie
4.  Update movie
5.  Stats
6.  Random movie
7.  Search movie
8.  Movies sorted by rating
9.  Movies sorted by year
10. Filter movies
11. Create rating histogram
12. Generate website
```

Enter the number of the option you want and follow the prompts.

### Examples

- **Add a movie:** choose `2`, then type a title such as `Inception`. The app fetches the year, rating, and poster automatically.
- **Generate the website:** choose `12` to create a `movies.html` file you can open in any browser.
- **Create a histogram:** choose `11` and enter a folder path; the chart is saved there as `movie_ratings_histogram.png`.

## Project Structure

| Path | Description |
| --- | --- |
| `main.py` | Entry point and menu logic |
| `movie_api.py` | Fetches movie data from the OMDb API |
| `generate_html.py` | Generates the HTML website from the database |
| `movie_storage/movie_storage_sql.py` | Database access layer (SQLAlchemy / SQLite) |
| `movie_storage/movie_storage.py` | JSON-based storage module |
| `data/movies.db` | SQLite database holding your movies |
| `data/movies.json` | JSON data file |
| `_static/movies_template.html` | HTML template used for the generated site |
| `_static/style.css` | Styling for the generated website |
| `movies.html` | The generated website (created by option 12) |
| `requirements.txt` | Python dependencies |

## Contributing

Contributions are welcome! If you'd like to improve the project:

1. Fork the repository.
2. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/my-feature
   ```
3. Commit your changes with a clear, descriptive message.
4. Push the branch to your fork and open a pull request.

Please keep the existing code style and add docstrings to new functions.
