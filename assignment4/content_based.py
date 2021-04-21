import pandas as pd
import numpy as np

path = "./MovieLens_1M/"

movie_header = ['MovieId', 'Title', 'Genre']
ratings_header = ['UserId', 'MovieId', 'Ratings', 'Timestamp']
user_header = ['UserId', 'Gender', 'Age', 'Occupation', 'ZipCode']

genre_counter_header = ['Genre', 'Amount']


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

    # Get every genre which were rated higher than 3
    genre_count = current_user_movies[current_user_movies[ratings_header[2]] > 3]
    # counted the genres and added to new dataframe
    genre_count = genre_count[genre_counter_header[0]].value_counts().to_frame(genre_counter_header[1]).reset_index()

    # renamed the column index to genre
    genre_count = genre_count.rename(columns={"index": genre_counter_header[0]})

    print (genre_count)

    return genre_count


def simple_contend_based():
    genre_count = countGenres()

    recommended_movies = moviesDf.merge(genre_count, how ="inner", on = "Genre")


    recommended_movies = recommended_movies.sort_values(by='Amount', ascending=False)

    print(recommended_movies[['Title', 'Genre']].head(15))


if __name__ == '__main__':
    moviesDf = pd.DataFrame(get_data(0))
    ratingsDf = pd.DataFrame(get_data(1))
    usersDf = pd.DataFrame(get_data(2))

    userid = get_user_id()

    # print the first 15 movies for the selected user
    show_first_fifteen_movies(userid)

    simple_contend_based()
