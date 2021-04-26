import pandas as pd
import numpy as np

path = "./MovieLens_1M/"

movie_header = ['MovieId', 'Title', 'Genre']
ratings_header = ['UserId', 'MovieId', 'Ratings', 'Timestamp']
user_header = ['UserId', 'Gender', 'Age', 'Occupation', 'ZipCode']
score_string = 'Score'
overlap_string = 'Overlap'

genre_counter_header = ['Genre', 'Amount']

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 1000)


def get_data(id):
    # needed to properly import the MovieLens-1M Dataset
    if id == 0:
        return pd.read_csv(path + 'movies.dat', sep='::', engine='python', header=None, names=movie_header,
                           index_col=movie_header[0])
    elif id == 1:
        return pd.read_csv(path + 'ratings.dat', sep='::', engine='python', header=None, names=ratings_header,
                           index_col=ratings_header[0])
    elif id == 2:
        return pd.read_csv(path + 'users.dat', sep='::', engine='python', header=None, names=user_header,
                           index_col=user_header[0])
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
    current_user = ratingsDf.loc[userid]
    # then merge with the movie-data to get the movie-information
    current_user_movies = current_user.merge(moviesDf, how='inner', on=movie_header[0])
    # and print the first 15 movies (only the title and the genre without index)

    print(current_user_movies)

    print(current_user_movies[[movie_header[1], movie_header[2]]].head(15).to_string(index=False))


def countGenres():
    # In SQL it would be SELECT * where user_id = x
    current_user = ratingsDf.loc[userid]
    # Create a true/false matrix for all movies, true if the user liked it
    liked_movies = current_user[current_user[ratings_header[2]] > 3]
    # filter the genreDf to only accept the liked movies
    genre_count = genreDf.loc[liked_movies[movie_header[0]]]
    # counted the genres and added to new dataframe
    genre_count = genre_count.sum(axis=0, skipna=True)

    print(genre_count)

    return genre_count


# This is just a simple content based algorithm.
# It only compares the determined genres from countGenres to the dataset, and give back Movies from the
# genre which were rated by the user.
# Additional, the values will be sorted by the Amount of the ratings.
def simple_content_based():
    # filter movies the user already rated
    current_user = ratingsDf.loc[userid]
    # sort the movies by the amount of the rated genres.
    recommended_movies = moviesDf.query('MovieId not in @current_user')
    recommended_movies[overlap_string] = calculate_overlap()
    recommended_movies[score_string] = recommended_movies[overlap_string]
    return recommended_movies


def simple_content_based_with_popularity():
    recommended_movies = simple_content_based()
    recommended_movies[score_string] = get_popularity()
    recommended_movies = recommended_movies.loc[recommended_movies[overlap_string] > 0]
    return recommended_movies


def get_popularity():
    return ratingsDf[[ratings_header[1], ratings_header[2]]].groupby(movie_header[0]).sum()


def calculate_overlap():
    genre_count = countGenres()
    # filter the genreDf based on the userprofile
    filtered_genreDf = genreDf.loc[:, genre_count > 0]
    return filtered_genreDf.sum(axis='columns')


def extended_content_based():
    # filter movies the user already rated
    current_user = ratingsDf.loc[userid]
    # sort the movies by the amount of the rated genres.
    recommended_movies = moviesDf.query('MovieId not in @current_user')
    weighted_genres = genreDf * countGenres()
    # replace 0 with nan for easier maths
    weighted_genres = weighted_genres.replace(0, np.nan).mean(axis='columns')
    recommended_movies['Popularity'] = get_popularity()
    # multiply the popularity with the squared genre-weight (and divide by 1000 to keep the numbers smaller
    recommended_movies[score_string] = recommended_movies['Popularity'] * (weighted_genres/100) ** 2
    return recommended_movies


if __name__ == '__main__':
    moviesDf = pd.DataFrame(get_data(0))
    ratingsDf = pd.DataFrame(get_data(1))
    usersDf = pd.DataFrame(get_data(2))
    # create a df that splits the genre column in the seperate columns
    genreDf = moviesDf.copy().pop(movie_header[2]).str.get_dummies(sep='|')
    userid = get_user_id()

    # print the first 15 movies for the selected user

    # show_first_fifteen_movies(userid)

    # here are the 3 algorithms
    # rec = simple_content_based()
    # rec = simple_content_based_with_popularity()
    rec = extended_content_based()

    rec = rec.sort_values(by=score_string, ascending=False)
    print(rec.head(10))
