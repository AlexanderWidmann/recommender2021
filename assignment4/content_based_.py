import pandas as pd
import numpy as np

path = "./MovieLens_1M/"

movie_header = ['MovieId', 'Title', 'Genre']
ratings_header = ['UserId', 'MovieId', 'Ratings', 'Timestamp']
user_header = ['UserId', 'Gender', 'Age', 'Occupation', 'ZipCode']

genre_counter_header = ['Genre', 'Amount']

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 1000)


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

    print(current_user_movies)

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

    print(genre_count)

    return genre_count


# This is just a simple content based algorithm.
# It only compares the determined genres from countGenres to the dataset, and give back Movies from the
# genre which were rated by the user.
# Additional, the values will be sorted by the Amount of the ratings.
def simple_content_based():
    # get the genres from the user.
    genre_count = countGenres()
    # Get the Movies from the genres which were rated by the given user.
    recommended_movies = moviesDf.merge(genre_count, how="inner", on="Genre")

    # sort the movies by the amount of the rated genres.
    recommended_movies = recommended_movies.sort_values(by='Amount', ascending=False)

    # print the first 15 Movies from the DataFrame.

    print("******* SIMPLE CONTENT BASED PREDICTION ****** ")

    print(recommended_movies[['Title', 'Genre']])

    return recommended_movies


def get_non_overlaped_Movies ():
    #Get the rated Movies
    current_user = ratingsDf[ratingsDf[user_header[0]] == userid]
    # then merge with the movie-data to get the movie-information
    current_user_movies = current_user.merge(moviesDf, how='inner', on=movie_header[0])

    #This two rows, do an Right Outer Join to get all movies which were not rated by the given user
    not_rated_Movies = pd.merge(current_user_movies, moviesDf, on=[movie_header[0]], how="outer", indicator=True)

    not_rated_Movies = not_rated_Movies[not_rated_Movies['_merge'] == "right_only"]

    return not_rated_Movies



def extended_content_based():
    # get the movies which were not rated by the given user
    recommended_movies = get_non_overlaped_Movies()

    # make an inner join with the ratings dataframe, so we can count the amount of ratings for each movie, that has
    # not been rated by the user
    recommended_movies = recommended_movies.merge(ratingsDf, on=movie_header[0], how="inner")

    # count the ratings
    count = pd.DataFrame(recommended_movies[movie_header[0]].value_counts().reset_index())

    count.columns = [movie_header[0], "rating_count"]

    i = pd.merge(count, moviesDf, how="inner", on=movie_header[0]).sort_values(by="rating_count", ascending=False)

    print(i[[movie_header[0], movie_header[1], movie_header[2], 'rating_count']].head(10))



if __name__ == '__main__':
    moviesDf = pd.DataFrame(get_data(0))
    ratingsDf = pd.DataFrame(get_data(1))
    usersDf = pd.DataFrame(get_data(2))

    userid = get_user_id()

    # print the first 15 movies for the selected user
    show_first_fifteen_movies(userid)
    extended_content_based()
