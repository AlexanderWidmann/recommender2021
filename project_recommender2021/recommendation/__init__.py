import json
import re
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

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


moviesDf = pd.DataFrame(get_data(0))
ratingsDf = pd.DataFrame(get_data(1))
genome_scoresDf = pd.DataFrame(get_data(2))
genome_tagsDf = pd.DataFrame(get_data(3))
tags_Df = pd.DataFrame(get_data(4))
movies_metaDataDf = pd.DataFrame(get_data(5))


def find_movies(movie_name):
    searched_movies = movies_metaDataDf[(
            movies_metaDataDf[movie_header[1]].str.contains(movie_name, regex=True, flags=re.IGNORECASE) |
            movies_metaDataDf['tmdb-keywords'].str.contains(movie_name, regex=True, flags=re.IGNORECASE) |
            movies_metaDataDf['directors'].str.contains(movie_name, regex=True, flags=re.IGNORECASE))]
    searched_movies.sort_values(by="avgRating", ascending=False, inplace=True)
    return searched_movies


def merge_tags():
    # merge with genome tags and score
    movies_scoresDf = pd.merge(moviesDf, genome_scoresDf, on=movie_header[0], how="inner")
    movies_tagsDf = pd.merge(movies_scoresDf, genome_tagsDf, on=genome_tags_header[0])

    movies_tagsDf.sort_values(inplace=True, by='relevance', ascending=False)

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


def to_JSON(df):
    json_movies = df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_movies)
    movies_context = {'d': data}
    return movies_context


def find_movie_by_id(id):
    id = int(id)
    movie = movies_metaDataDf[movies_metaDataDf['MovieId'] == id]
    return movie


def algo1(id):
    tmp_movies = movies_metaDataDf
    movie = find_movie_by_id(id)
    # this is necessary, because otherwise the SequenceMatcher thinks that NaN is a float Number
    tmp_movies['tmdb-keywords'].replace(np.NaN, " ", inplace=True)
    # tmp_movies['tmdb-keywords'].replace("\d", np.nan, inplace=True)
    keywords = movie['tmdb-keywords'].iloc[0]

    tmp_movies['similarity'] = tmp_movies['tmdb-keywords'].apply(lambda x: SequenceMatcher(None, keywords, x).ratio())
    tmp_movies.sort_values(by="similarity", inplace=True, ascending=False)
    print(tmp_movies[["title", "similarity", "tmdb-keywords"]].head(15))

    return tmp_movies


def similiarMovieKeywords(id):
    tmp_movies = movies_metaDataDf
    movie = find_movie_by_id(id)
    tmp_movies['tmdb-keywords'].dropna(inplace=True)
    tmp_movies['tmdb-keywords'].replace(np.NaN, " ", inplace=True)
    pattern = re.compile(r"\W+")
    keywords = movie['tmdb-keywords'].iloc[0]
    keywords = pattern.sub(" ", keywords)
    set_keywords = set(keywords.split(" "))
    # len(set(pattern.sub(" ",tmp_movies['tmdb-keywords'].iloc[0]).split(" ")).intersection(set_keywords))
    tmp_movies['overlap'] = tmp_movies["tmdb-keywords"].apply(lambda x: calcOverlap(x, set_keywords))
    tmp_movies.sort_values(by="overlap", ascending=False, inplace=True)

    return to_JSON(tmp_movies.head(20))


def similiarMovieActors(id):
    tmp_movies = movies_metaDataDf
    movie = find_movie_by_id(id)
    tmp_movies['actors'].dropna(inplace=True)
    tmp_movies['actors'].replace(np.NaN, " ", inplace=True)
    pattern = re.compile(r"\W+")
    keywords = movie['actors'].iloc[0]
    keywords = pattern.sub(" ", keywords)
    set_keywords = set(keywords.split(" "))
    # len(set(pattern.sub(" ",tmp_movies['tmdb-keywords'].iloc[0]).split(" ")).intersection(set_keywords))
    tmp_movies['overlap'] = tmp_movies["actors"].apply(lambda x: calcOverlap(x, set_keywords))
    tmp_movies.sort_values(by="overlap", ascending=False, inplace=True)

    return to_JSON(tmp_movies.head(20))


def calcOverlap(x, set_keywords):
    pattern = re.compile(r"\W+")
    keywords = pattern.sub(" ", x)
    tmp_set_keywords = set(keywords.split(" "))
    return len(tmp_set_keywords.intersection(set_keywords))


def getData():
    return moviesDf,ratingsDf, genome_scoresDf, genome_tagsDf, tags_Df, movies_metaDataDf


if __name__ == '__main__':
    # algo1(1)
    # print(similiarMovieKeywords(1))
    print(similiarMovieActors(1))
