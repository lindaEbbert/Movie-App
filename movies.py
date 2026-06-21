from fuzzywuzzy import process
from random import randrange
import matplotlib
import movie_storage
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def get_dispatcher():
    return {
        "0": print_goodbye_message,
        "1": print_all_movies,
        "2": add_movie,
        "3": delete_movie,
        "4": update_movie,
        "5": print_statistics,
        "6": print_random_movie,
        "7": search_movie,
        "8": print_movies_sorted_by_rating,
        "9": print_movies_sorted_by_year,
        "10": print_filtered_movies,
        "11": create_histogram
    }


def get_info_from_all_movies(key):
    movies = movie_storage.get_movies()
    info_list = []
    for movie in movies:
        info_list.append(movie[key])
    return info_list


def get_index_by_title(title):
    all_movie_titles = get_info_from_all_movies("title")
    return all_movie_titles.index(title)


def get_movie_info_by_title(title, info_key):
    movies = movie_storage.get_movies()
    movie_index = get_index_by_title(title)
    return movies[movie_index][info_key]


def get_sorted_movies_by_key(sorting_key, descending=True):
    sorted_movies = []
    unsorted_movies = movie_storage.get_movies()
    while len(unsorted_movies) > 0:  # as long as our original list in unsorted_list isn't empty...
        max_value = unsorted_movies[0][sorting_key]
        index_of_max = 0
        for i in range(1,len(unsorted_movies)):  # ... it takes the one with the highest value...
            if unsorted_movies[i][sorting_key] > max_value:
                max_value = unsorted_movies[i][sorting_key]
                index_of_max = i
        sorted_movies.append(unsorted_movies[index_of_max])  # ... and transfers it to the end of our sorted_list
        del unsorted_movies[index_of_max]
    if descending:
        return sorted_movies
    else:
        return sorted_movies[::-1]


def print_movies_sorted_by_rating():
    sorted_movies = get_sorted_movies_by_key("rating")
    for movie in sorted_movies:
        print(f"{movie["title"]} ({movie["year"]}): {movie["rating"]}")


def get_users_choice_y_or_no():
    while True:
        users_choice = input('Do you want the latest movies first? (Y/N) \x1b[32m')
        if users_choice.upper() == "Y":
            return True
        elif users_choice.upper() == "N":
            return False
        else:
            print('\x1b[31mPlease enter "Y" or "N"\x1b[0m')


def print_movies_sorted_by_year():
    is_descending = get_users_choice_y_or_no()
    sorted_movies = get_sorted_movies_by_key("year", is_descending)
    print("\x1b[0m")
    for movie in sorted_movies:
        print(f"{movie["title"]} ({movie["year"]}): {movie["rating"]}")


def get_matching_movies(search_string):
    matching_movies = []
    for title in get_info_from_all_movies("title"):
        string_is_in_title = search_string.lower() in title.lower()
        if string_is_in_title:
            matching_movies.append(title)
    return matching_movies


def check_for_similar_movies(search_string):
    movies = movie_storage.get_movies()
    all_movies = get_info_from_all_movies("title")
    similar_movies = process.extract(search_string, all_movies, limit=3)
    similar_movies_list = []
    for movie, _similarity_metric in similar_movies:
        movie_index = get_index_by_title(movie)
        similar_movies_list.append(movies[movie_index])
    return similar_movies_list


def search_movie():
    # get search string
    is_valid_input = False
    search_string = "Placeholder Search String"
    while not is_valid_input:
        search_string = input("Enter part of movie name: \x1b[32m")
        if search_string == "":
            print("\x1b[31mEmpty search sting not allowed!\x1b[0m")
        else:
            is_valid_input = True
    # compare to movie titles
    matching_movies_list = get_matching_movies(search_string)
    if len(matching_movies_list) > 0:
        for title in matching_movies_list:
            print(f"\x1b[0m{title}: {get_movie_info_by_title(title, "rating")}")
    else:
        similar_movies = check_for_similar_movies(search_string)
        print(f"\x1b[0mThe movie {search_string} does not exist. Did you mean:")
        for movie in similar_movies:
            print(f"{movie["title"]}: {movie["rating"]}")


def get_random_movie_title():
    list_of_titles = get_info_from_all_movies("title")
    number_of_total_movies = len(list_of_titles)
    random_index = randrange(0, number_of_total_movies)
    random_movie = list_of_titles[random_index]
    return random_movie


def print_random_movie():
    random_movie = get_random_movie_title()
    rating_of_random_movie = get_movie_info_by_title(random_movie,"rating")
    print(f"Your movie for tonight: {random_movie}, it's rated {rating_of_random_movie}")


def get_mean_of_ratings():
    all_ratings = get_info_from_all_movies("rating")
    return sum(all_ratings) / len(all_ratings)


def get_median_of_ratings(sorted_movies):
    number_of_total_movies = len(sorted_movies)
    movie_number_is_odd = number_of_total_movies % 2 == 0
    half = number_of_total_movies // 2
    if movie_number_is_odd:
        first_middle_movie_rating = sorted_movies[half - 1]["rating"]
        second_middle_movie_rating = sorted_movies[half + 1]["rating"]
        middle_value = (first_middle_movie_rating + second_middle_movie_rating) / 2
    else:
        middle_value = sorted_movies[half]["rating"]
    return middle_value


def get_best_and_worst_movies_infos(sorted_movies):
    best_movie_rating = sorted_movies[0]["rating"]
    worst_movie_rating = sorted_movies[-1]["rating"]
    best_movies = []
    worst_movies = []
    for movie in sorted_movies:
        if movie["rating"] == best_movie_rating:
            best_movies.append(movie)
        elif movie["rating"] == worst_movie_rating:
            worst_movies.append(movie)
    return best_movies, worst_movies


def print_best_or_worst_movies(movie_list, best=True):
    if best:
        print("Best movie:", end=" ")
    else:
        print("Worst movie:", end=" ")
    for movie in movie_list:
        print(movie["title"], end=", ")
    print(movie_list[0]["rating"])


def print_statistics():
    # average
    average_rating = get_mean_of_ratings()
    print(f"Average rating: {average_rating}")
    sorted_movies = get_sorted_movies_by_key("rating")
    # median
    median_rating = get_median_of_ratings(sorted_movies)
    print(f"Median rating: {median_rating}")
    # best and worst
    best_movie, worst_movie = get_best_and_worst_movies_infos(sorted_movies)
    print_best_or_worst_movies(best_movie)
    print_best_or_worst_movies(worst_movie, best=False)


def update_movie():
    title_to_update = get_user_input_title()
    all_movie_titles = get_info_from_all_movies("title")
    title_is_in_database = title_to_update in all_movie_titles
    if title_is_in_database:
        updated_rating = float(input("\x1b[0mEnter new movie rating (0-10): \x1b[32m"))
        movie_storage.update_movie(title_to_update, updated_rating)
        print(f"\x1b[0mMovie {title_to_update} successfully updated")
    else:
        print(f"\x1b[31mMovie {title_to_update} doesn't exist!\x1b[0m")


def delete_movie():
    movie_to_delete = get_user_input_title("Enter movie name to delete: \x1b[32m")
    all_movie_titles = get_info_from_all_movies("title")
    is_in_movies = movie_to_delete in all_movie_titles
    if is_in_movies:
        movie_storage.delete_movie(movie_to_delete)
        print(f"\x1b[0mMovie {movie_to_delete} successfully deleted")
    else:
        print(f"\x1b[31mMovie {movie_to_delete} not found!\x1b[0m")


def check_input_is_valid(user_input, type_of_input):
    is_not_empty = user_input != ""
    if type_of_input == "title":
        if is_not_empty:
            return True
        else:
            print("\x1b[31mEmpty Strings are not allowed!\x1b[0m")
    elif type_of_input == "rating":
        if 0 <= user_input <= 10:
            return True
        else:
            print("\x1b[31mRating must be between 0 and 10!\x1b[0m")
    elif type_of_input == "year":
        if 1888 <= user_input <= 9999:
            return True
        else:
            print("\x1b[31mYear must be between 1888 and 9999!\x1b[0m")
    return False


def get_user_input_title(prompt_string="Enter movie title: \x1b[32m"):
    title_is_valid = False
    title = "Placeholder Title"
    while not title_is_valid:
        title = input(prompt_string)
        title_is_valid = check_input_is_valid(title, "title")
    return title


def get_user_input_year(prompt_string="\x1b[0mEnter new movie year: \x1b[32m"):
    year_is_valid = False
    year = "Placeholder Year"
    while not year_is_valid:
        try:
            year = int(input(prompt_string))
        except ValueError:
            print("\x1b[31mThat's not a year, try again.\x1b[0m")
        else:
            year_is_valid = check_input_is_valid(year, "year")
    return year


def get_user_input_rating(prompt_string="\x1b[0mEnter new movie rating (0-10): \x1b[32m"):
    rating_is_valid = False
    rating = "Placeholder Rating"
    while not rating_is_valid:
        try:
            rating = float(input(prompt_string))
        except ValueError:
            print("\x1b[31mThat's an invalid rating, try again.\x1b[0m")
        else:
            rating_is_valid = check_input_is_valid(rating, "rating")
    return rating


def add_movie():
    title = get_user_input_title()
    rating = get_user_input_rating()
    year = get_user_input_year()
    movie_storage.add_movie(title, year, rating)
    print(f"\x1b[0mMovie {title} successfully added")


def number_movies_in_database():
    movies = movie_storage.get_movies()
    return len(movies)


def print_all_movies():
    movies = movie_storage.get_movies()
    print(f"{number_movies_in_database()} movies in total")
    for movie in movies:
        print(f"{movie["title"]} ({movie["year"]}): {movie["rating"]}")


def plot_histogram():
    fig, ax = plt.subplots()
    ratings_list = get_info_from_all_movies("rating")
    ax.hist(ratings_list)
    return fig


def create_histogram():
    output_path = input("Path to save your histogram: \x1b[32m")
    filename = "movie_ratings_histogram.png"
    if output_path[-1] == "/":
        complete_path = output_path + filename
    else:
        complete_path = output_path + "/" + filename
    rating_hist = plot_histogram()
    rating_hist.savefig(complete_path)
    print(f"\x1b[0mHistogram successfully saved: {complete_path}")


def print_goodbye_message():
    print("\x1b[93m\nBye!\x1b[0m")


def execute_users_choice(users_choice):
    dispatcher = get_dispatcher()
    dispatcher[str(users_choice)]()
    input("\nPress enter to continue")
    print()


def get_user_input_choice(prompt_string="\nEnter choice (0-11): \x1b[32m"):
    is_valid_input = False
    users_choice = "Placeholder Choice"
    while not is_valid_input:
        try:
            users_choice = int(input(prompt_string))
        except ValueError:
            print("\x1b[31mInvalid input!\x1b[0m")
        else:
            is_valid_input = str(users_choice) in get_dispatcher().keys()
            if not is_valid_input:
                print("\x1b[31mOption not implemented!\x1b[0m")
            print("\x1b[0m", end="")
    return users_choice


def print_title():
    print("\x1b[94m********** My Movies Database **********\n\x1b[0m")


def filter_movies(min_rating, start_year, end_year):
    movies = movie_storage.get_movies()
    filtered_movies = []
    for movie in movies:
        rating_is_okay = movie["rating"] >= min_rating
        year_is_okay = end_year >= movie["year"] >= start_year
        if rating_is_okay and year_is_okay:
            filtered_movies.append(movie)
    return filtered_movies


def get_user_input_filter_params():
    # get min rating
    while True:
        min_rating = input("\x1b[0mEnter minimum rating (leave blank for no minimum rating): \x1b[32m")
        if min_rating == "":
            min_rating = 0
            break
        try:
            min_rating = int(min_rating)
        except ValueError:
            print("\x1b[31mInvalid input!\x1b[0m")
        else:
            if 0 <= min_rating <= 10:
                break
            else:
                print("\x1b[31mInvalid input: Number must be between 0 and 10!\x1b[0m")
    # get start year
    while True:
        start_year = input("\x1b[0mEnter start year (leave blank for no start year): \x1b[32m")
        if start_year == "":
            start_year = 0
            break
        try:
            start_year = int(start_year)
        except ValueError:
            print("\x1b[31mInvalid input!\x1b[0m")
        else:
            if 1888 <= start_year <= 9999:
                break
            else:
                print("\x1b[31mInvalid input: Year must be between 1888 and 9999!\x1b[0m")
    # get max year
    while True:
        end_year = input("\x1b[0mEnter end year (leave blank for no end year): \x1b[32m")
        if end_year == "":
            end_year = 9999
            break
        try:
            end_year = int(end_year)
        except ValueError:
            print("\x1b[31mInvalid input!\x1b[0m")
        else:
            if 1888 <= end_year <= 9999:
                break
            else:
                print("\x1b[31mInvalid input: Year must be between 1888 and 9999!\x1b[0m")
    return min_rating, start_year, end_year


def print_filtered_movies():
    min_rating, min_year, max_year = get_user_input_filter_params()
    filtered_movies = filter_movies(min_rating, min_year, max_year)
    print("\x1b[0m")
    for movie in filtered_movies:
        print(f"{movie['title']} ({movie['year']}): {movie['rating']}")


def print_menu():
    print("\x1b[94mMenu:")
    print("0.  Exit")
    print("1.  List movies")
    print("2.  Add movie")
    print("3.  Delete movie")
    print("4.  Update movie")
    print("5.  Stats")
    print("6.  Random movie")
    print("7.  Search movie")
    print("8.  Movies sorted by rating")
    print("9.  Movies sorted by year")
    print("10. Filter movies")
    print("11. Create rating histogram\x1b[0m")


def main():
    print_title()
    quit_program = False
    while not quit_program:
        print_menu()
        users_choice = get_user_input_choice()
        if users_choice == 0:
            quit_program = True
            print_goodbye_message()
        else:
            print()
            execute_users_choice(users_choice)


if __name__ == "__main__":
    main()
