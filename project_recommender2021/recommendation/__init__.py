import json
import re
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.sparse import load_npz

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 20)

movie_header = ['movieId', 'title', 'genres']
ratings_header = ['userId', 'movieId', 'ratings', 'timestamp']
genome_scores_header = ['movieId', 'tagId', 'relevance']
genome_tags_header = ['tagId', 'tag']
tags_header = ['userId,movieId,tag,timestamp']

p = Path(__file__).parent
path = p.joinpath('ml-25m')
path_sample = p.joinpath('ml-25m-sample')

AmountRows = 10000


def get_data(id):
    # needed to properly import the MovieLens-25M Dataset
    if id == 0:
        return pd.read_csv(path.joinpath('movies.csv'), engine='python', nrows=AmountRows)
    elif id == 1:
        return pd.read_csv(path.joinpath('ratings.csv'), engine='python', nrows=AmountRows)
    elif id == 2:
        return pd.read_csv(path.joinpath('genome-scores.csv'), engine='python', nrows=AmountRows)
    elif id == 3:
        return pd.read_csv(path.joinpath('genome-tags.csv'), engine='python', nrows=AmountRows)
    elif id == 4:
        return pd.read_csv(path.joinpath('tags.csv'), engine='python', nrows=AmountRows)
    elif id == 5:
        return pd.read_csv(path.joinpath('custom_metadata.csv'), engine="python", nrows=AmountRows)
    else:
        return


def get_sample_data(id):
    if id == 0:
        return pd.read_csv(path_sample.joinpath('movies-sample.csv'), engine='python')
    elif id == 1:
        return pd.read_csv(path_sample.joinpath('ratings-sample.csv'), engine='python', nrows=AmountRows)
    elif id == 2:
        return pd.read_csv(path_sample.joinpath('genome-score-sample.csv'), engine='python', nrows=AmountRows)
    elif id == 3:
        return pd.read_csv(path_sample.joinpath('genome-tags-sample.csv'), engine='python', nrows=AmountRows)
    elif id == 4:
        return pd.read_csv(path_sample.joinpath('tags-sample.csv'), engine='python', nrows=AmountRows)
    elif id == 5:
        return pd.read_csv(path_sample.joinpath('links.csv'), engine="python")
    elif id == 6:
        return pd.read_csv(path_sample.joinpath('movies_metadata.csv'), engine="python")

    else:
        return


def load_similarity():
    return load_npz(path.joinpath('similarity_matrix.npz'))


moviesDf = pd.DataFrame(get_data(0))
ratingsDf = pd.DataFrame(get_data(1))
genome_scoresDf = pd.DataFrame(get_data(2))
genome_tagsDf = pd.DataFrame(get_data(3))
tags_Df = pd.DataFrame(get_data(4))
movies_metaDataDf = pd.DataFrame(get_data(5))

similarity = load_similarity()


def find_movies(movie_name):
    searched_movies = movies_metaDataDf[(
            movies_metaDataDf[movie_header[1]].str.contains(movie_name, regex=True, flags=re.IGNORECASE) |
            movies_metaDataDf['tmdb-keywords'].str.contains(movie_name, regex=True, flags=re.IGNORECASE) |
            movies_metaDataDf['directors'].str.contains(movie_name, regex=True, flags=re.IGNORECASE))]
    searched_movies = searched_movies.sort_values(by="avgRating", ascending=False)
    return searched_movies


def merge_tags():
    # merge with genome tags and score
    movies_scoresDf = pd.merge(moviesDf, genome_scoresDf, on=movie_header[0], how="inner")
    movies_tagsDf = pd.merge(movies_scoresDf, genome_tagsDf, on=genome_tags_header[0])

    movies_tagsDf = movies_tagsDf.sort_values(by='relevance', ascending=False)

    grouped_movies = movies_tagsDf.groupby(movie_header[0]).head(20)

    return grouped_movies


def movie_json(movie_name):
    # find the movies based on movie_name
    searched_movies = find_movies(movie_name=movie_name)

    # replace | with comma in genres
    searched_movies[movie_header[2]] = searched_movies[movie_header[2]].str.replace("|", ',')
    # Remove the release year
    searched_movies[movie_header[1]] = searched_movies[movie_header[1]].str.replace("[^a-zA-Z\s]", "")
    return to_JSON(df=searched_movies)


# Transform a df to a JSON-File,in order to be able to process it better in the frontend
def to_JSON(df):
    json_movies = df.reset_index().to_json(orient='records')
    data = json.loads(json_movies)
    movies_context = {'d': data}
    return movies_context


def find_movie_by_id(id):
    id = int(id)
    movie = movies_metaDataDf[movies_metaDataDf['MovieId'] == id]
    return movie


# simpleMetaMulitplicated_recommender: genre, popularity, actors and directors
def simpleMetaMulitplicated_recommender(id, amount=20):
    tmp_movies = movies_metaDataDf
    tmp_movies['similarity'] = getGenreOverlap(id) * similiarMovieActorsOrDirectors(
        id) * similiarMovieActorsOrDirectors(id, 'directors') * getPopularity()
    tmp_movies = tmp_movies.sort_values(by="similarity", ascending=False)
    tmp_movies = tmp_movies.drop(tmp_movies[tmp_movies['MovieId'] == int(id)].index)
    return to_JSON(tmp_movies.head(amount))


# same as the multiplicated one, but the sum of the recommenders instead of multiplication
def simpleMeta_recommender(id, amount=20):
    tmp_movies = movies_metaDataDf
    tmp_movies['similarity'] = getGenreOverlap(id) + similiarMovieActorsOrDirectors(
        id) + similiarMovieActorsOrDirectors(id, 'directors') + getPopularity()
    tmp_movies = tmp_movies.sort_values(by="similarity", ascending=False)
    tmp_movies = tmp_movies.drop(tmp_movies[tmp_movies['MovieId'] == int(id)].index)
    return to_JSON(tmp_movies.head(amount))


# uses all algorithms and allows factors to adjust the importance
def allAlgorithmsWithOptionalFactors_recommender(id, amount=20, genre_factor=1, actors_factor=1, directors_factor=1,
                                                 popularity_factor=1, pattern_factor=1, keywords_factor=1,
                                                 rating_factor=1, summary_factor=1):
    id = int(id)
    tmp_movies = movies_metaDataDf
    tmp_movies['similarity'] = genre_factor * getGenreOverlap(id) + actors_factor * similiarMovieActorsOrDirectors(id) + directors_factor * similiarMovieActorsOrDirectors(id, 'directors') + popularity_factor * getPopularity()
    tmp_movies['similarity'] = tmp_movies['similarity'] + pattern_factor * similarMoviesPattern(id) + keywords_factor * similiarMovieKeywords(
        id) + rating_factor * similarMovieRatings(id) + summary_factor * similarMovieSummary(id)
    tmp_movies = tmp_movies.sort_values(by="similarity", ascending=False)
    tmp_movies = tmp_movies.drop(tmp_movies[tmp_movies['MovieId'] == int(id)].index)
    return to_JSON(tmp_movies.head(amount))


def getPopularity():
    tmp_movies = movies_metaDataDf
    tmp_movies['similarity'] = tmp_movies['avgRating'] * tmp_movies['numRatings']
    tmp_movies['similarity'] = tmp_movies['similarity'].divide(max(tmp_movies['similarity']))
    return tmp_movies['similarity']


# the actual recommender that returns the top amount of movies
def similarMoviesPattern_recommender(id, amount=20):
    tmp_movies = movies_metaDataDf
    tmp_movies['similarity'] = similarMoviesPattern(id)
    tmp_movies = tmp_movies.sort_values(by="similarity", ascending=False)
    tmp_movies = tmp_movies.drop(tmp_movies[tmp_movies['MovieId'] == int(id)].index)
    return to_JSON(tmp_movies.head(amount))


# finds the similar movie based on pattern in keywords
def similarMoviesPattern(id):
    tmp_movies = movies_metaDataDf
    movie = find_movie_by_id(id)
    # this is necessary, because otherwise the SequenceMatcher thinks that NaN is a float Number
    tmp_movies['tmdb-keywords'] = tmp_movies['tmdb-keywords'].replace(np.NaN, " ")
    # tmp_movies['tmdb-keywords'].replace("\d", np.nan, inplace=True)
    keywords = movie['tmdb-keywords']

    tmp_movies['similarity'] = tmp_movies['tmdb-keywords'].apply(lambda x: SequenceMatcher(None, keywords, x).ratio())
    tmp_movies['similarity'] = tmp_movies['similarity'].divide(max(tmp_movies['similarity']))
    return tmp_movies['similarity'].fillna(0)


def similarMovieKeywords_recommender(id, amount=20):
    tmp_movies = movies_metaDataDf
    tmp_movies['similarity'] = similiarMovieKeywords(int(id))
    tmp_movies = tmp_movies.sort_values(by="similarity", ascending=False)
    tmp_movies = tmp_movies.drop(tmp_movies[tmp_movies['MovieId'] == int(id)].index)
    return to_JSON(tmp_movies.head(amount))


# finds similar movies based on the amount of overlaping keywords
def similiarMovieKeywords(id):
    tmp_movies = movies_metaDataDf
    movie = find_movie_by_id(id)
    # Drop rows which don't contain any keywords
    tmp_movies['tmdb-keywords'] = tmp_movies['tmdb-keywords'].dropna()
    # Replace NaN with space, otherwise pandas assumes that NaN is a float value. This leads to an exception
    tmp_movies['tmdb-keywords'] = tmp_movies['tmdb-keywords'].replace(np.NaN, " ")
    # Remove all braces, commas etc
    pattern = re.compile(r"\W+")
    # get the keywords as string
    keywords = movie['tmdb-keywords'].iloc[0]
    keywords = pattern.sub(" ", keywords)
    # create a set of keywords
    set_keywords = set(keywords.split(" "))

    tmp_movies['similarity'] = tmp_movies["tmdb-keywords"].apply(lambda x: calcOverlap(x, set_keywords))
    tmp_movies['similarity'] = tmp_movies['similarity'].divide(max(tmp_movies['similarity']))
    return tmp_movies['similarity'].fillna(0)


def similarMovieActors_recommender(id, amount=20):
    tmp_movies = movies_metaDataDf
    tmp_movies['similarity'] = similiarMovieActorsOrDirectors(id)
    tmp_movies = tmp_movies.sort_values(by="similarity", ascending=False)
    tmp_movies = tmp_movies.drop(tmp_movies[tmp_movies['MovieId'] == int(id)].index)
    return to_JSON(tmp_movies.head(amount))


# finds similar movies based on the amount of overlaping Actors
def similiarMovieActorsOrDirectors(id, col_name='actors'):
    tmp_movies = movies_metaDataDf
    movie = find_movie_by_id(id)
    tmp_movies[col_name] = tmp_movies[col_name].dropna()
    tmp_movies[col_name] = tmp_movies[col_name].replace(np.NaN, " ")
    pattern = re.compile(r"\W+")
    keywords = movie[col_name].iloc[0]
    keywords = pattern.sub(" ", keywords)
    set_keywords = set(keywords.split(" "))
    # len(set(pattern.sub(" ",tmp_movies['tmdb-keywords'].iloc[0]).split(" ")).intersection(set_keywords))
    tmp_movies['similarity'] = tmp_movies[col_name].apply(lambda x: calcOverlap(x, set_keywords))
    tmp_movies['similarity'] = tmp_movies['similarity'].divide(max(tmp_movies['similarity']))
    return tmp_movies['similarity'].fillna(0)


def similarMovieSummary_recommender(id, amount=20):
    tmp_movies = movies_metaDataDf
    tmp_movies['similarity'] = similarMovieSummary(id)
    tmp_movies = tmp_movies.sort_values(by="similarity", ascending=False)
    tmp_movies = tmp_movies.drop(tmp_movies[tmp_movies['MovieId'] == int(id)].index)
    return to_JSON(tmp_movies.head(amount))


def similarMovieSummary(id):
    tmp_movies = movies_metaDataDf
    index = tmp_movies[tmp_movies['MovieId'] == int(id)].index[0]

    # get similarities for this movie
    # use .toarray() to convert from sparse matrix
    # use [0] to convert "matrix" with only one row to one-dimensional array
    similarities = similarity[index].toarray()[0]
    tmp_movies['similarity'] = similarities[:AmountRows]
    return tmp_movies['similarity'].fillna(0)


def similarMovieRatings_recommender(id, amount=20):
    tmp_movies = movies_metaDataDf
    tmp_movies['similarity'] = similarMovieRatings(int(id))
    tmp_movies = tmp_movies.sort_values(by="similarity", ascending=False)
    tmp_movies = tmp_movies.drop(tmp_movies[tmp_movies['MovieId'] == int(id)].index)
    return to_JSON(tmp_movies.head(amount))


def similarMovieRatings(id):
    tmp_movies = movies_metaDataDf['MovieId']

    # Create the pivot table / matrix
    movies_ratings_pivot = ratingsDf.pivot_table(index="movieId", columns="userId", values="rating", fill_value=0)

    # Get the Ratings from the selected Movie
    ratings_movie = movies_ratings_pivot[id]

    # Calculate the Similiarty between the Ratings-subsets
    similiar_movies = movies_ratings_pivot.corrwith(ratings_movie)

    # Drop NaN Values
    similiar_movies = similiar_movies.dropna()
    # Cast to DataFrame
    similiar_movies_df = pd.DataFrame({"movieId": similiar_movies.index, "similarity": similiar_movies.values})

    # Merge with MetaDataDf to get the proper indexes to easily reuse the data
    merged_movies = pd.merge(tmp_movies, similiar_movies_df, right_on="movieId", left_on="MovieId", how="left")
    merged_movies['similarity'] = merged_movies['similarity'].divide(max(merged_movies['similarity']))
    return merged_movies['similarity'].fillna(0)


# different algoritmn for the ratings
def similarMovieUserRatings_recommender(id, amount=20):
    tmp_movies = movies_metaDataDf
    tmp_movies['similarity'] = similarMovieRatings(int(id))
    tmp_movies = tmp_movies.sort_values(by="similarity", ascending=False)
    tmp_movies = tmp_movies.drop(tmp_movies[tmp_movies['MovieId'] == int(id)].index)
    return to_JSON(tmp_movies.head(amount))


def similarMovieUserRatings(id):
    tmp_movies = movies_metaDataDf
    min_rating = 3
    relevant_users = ratingsDf[ratingsDf['movieId'] == id]
    relevant_users = relevant_users[relevant_users['rating'] > min_rating]

    # filter the rest of the ratings to only the userIds that are chosen as relevant are present
    movies = ratingsDf[ratingsDf['movieId'] != id]
    movies = movies[movies['userId'].isin(relevant_users['userId'])]
    movies = movies[['movieId', 'rating']]
    movies = movies[movies['rating'] > min_rating]
    movies = movies.groupby('movieId').agg(['mean', 'count'])
    movies.columns = ['_'.join(str(i) for i in col) for col in movies.columns]
    movies = movies.reset_index()
    # simple criteria to also factor in the amount of ratings (only with the weight 0.25 per count)
    movies['similarity'] = movies['rating_mean'] * (0.75 + movies['rating_count'] / 4)
    # Merge with MetaDataDf to get the proper indexes to easily reuse the data
    merged_movies = pd.merge(tmp_movies['MovieId'], movies[['movieId', 'similarity']], right_on="movieId",
                             left_on="MovieId",
                             how="left")
    # to get a value between 0 and 1
    merged_movies['similarity'] = merged_movies['similarity'].divide(max(merged_movies['similarity']))
    return merged_movies['similarity'].fillna(0)


def getGenreOverlap(id):
    tmp_movies = movies_metaDataDf[['MovieId', 'genres']].copy()
    movie_genres = eval(find_movie_by_id(id)['genres'].iloc[0])
    tmp_movies['similarity'] = tmp_movies['genres'].apply(lambda x: calcListOverlap(eval(x), movie_genres))
    tmp_movies['similarity'] = tmp_movies['similarity'].divide(max(tmp_movies['similarity']))
    return tmp_movies['similarity'].fillna(0)


def calcListOverlap(listA, listB):
    return len(list(set(listA).intersection(set(listB))))


def calcOverlap(x, set_keywords):
    # Remove braces, commas etc.
    pattern = re.compile(r"\W+")
    keywords = pattern.sub(" ", x)
    tmp_set_keywords = set(keywords.split(" "))
    # Check if there is any overlap, and count the amount of overlaps
    return len(tmp_set_keywords.intersection(set_keywords))


def getData():
    # returns all the data, which is necessary for other files
    return moviesDf, ratingsDf, genome_scoresDf, genome_tagsDf, tags_Df, movies_metaDataDf


if __name__ == '__main__':
    # print(similiarMovieKeywords(1))
    # print(similiarMovieActors(1))
    # summarySimilarity(5378)
    # print(movies_metaDataDf[movies_metaDataDf['MovieId'] == 100].index[0])
    # print(similiarMoviesPattern_recommender(1))
    # similarMovieRatings_recommender(1)
    # similarMovieRatings_recommender(1)
    print(allAlgorithmsWithOptionalFactors_recommender(1))
