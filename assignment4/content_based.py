import pandas as pd
import numpy as np

path = "./MovieLens_1M/"

movie_header = ['MovieId', 'Title', 'Genre']
ratings_header = ['UserId', 'MovieId', 'Ratings', 'Timestamp']
user_header = ['UserId', 'Gender', 'Age', 'Occupation', 'ZipCode']

genre_counter_header = ['UserId', 'Genre', 'Amount']


def get_data(id):
    # needed to properly import the MovieLens-1M Dataset
    if id == 0:
        return pd.read_csv(path + 'movies.dat', sep='::', engine='python', header=None, names=movie_header)
    elif id == 1:
        return pd.read_csv(path + 'ratings.dat', sep='::', engine='python', header=None, names=ratings_header)
    elif id == 2:
        return pd.read_csv(path + 'users.dat', sep='::', engine='python', header=None, names=user_header)
    else:
        return


def get_user_id() -> int:
    try:
        print('Select an UserId:')
        selected_userid = int(input())
        if selected_userid < 1 or selected_userid > 6040:
            print('Invalid ID')
            selected_userid = get_user_id()
    except ValueError:
        print('Try again! With a proper ID')
        selected_userid = get_user_id()
    return selected_userid


# SHOW FIRST 15 MOVIES + GENRES WICH WERE RATED BY THE GIVEN USER
def show_first_fifteen_movies(userid):
    # Select the movies which where rated by the given user
    # In SQL it would be SELECT * where user_id = x
    current_user = ratingsDf[ratingsDf[user_header[0]] == userid]
    # then merge with the movie-data to get the movie-information
    current_user_movies = current_user.merge(moviesDf, how='inner', on=movie_header[0])
    # and print the first 15 movies (only the title and the genre without index)
    print(current_user_movies[[movie_header[1], movie_header[2]]].head(15).to_string(index=False))


def countGenres():
    # In SQL it would be SELECT * where user_id = x
    current_user = ratingsDf[ratingsDf[user_header[0]] == userid]
    # then merge with the movie-data to get the movie-information
    current_user_movies = current_user.merge(moviesDf, how='inner', on=movie_header[0])

    genre_count = current_user_movies[current_user_movies[ratings_header[2]] > 3]
    genre_count = genre_count['Genre'].value_counts()

    print(genre_count)

    return


def split(x):
    y = x.split("|")
    return y


if __name__ == '__main__':
    moviesDf = pd.DataFrame(get_data(0))
    ratingsDf = pd.DataFrame(get_data(1))
    usersDf = pd.DataFrame(get_data(2))

    userid = get_user_id()

    # print the first 15 movies for the selected user
    show_first_fifteen_movies(userid)

    countGenres()
