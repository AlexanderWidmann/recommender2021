import json
import re
from pathlib import Path

import pandas as pd

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 30)

movie_header = ['MovieId', 'Title', 'Genre']
ratings_header = ['UserId', 'MovieId', 'Ratings', 'Timestamp']
user_header = ['UserId', 'Gender', 'Age', 'Occupation', 'ZipCode']

p = Path(__file__).parent
path = p.joinpath('MovieLens_1M')


def get_data(id):
    # needed to properly import the MovieLens-1M Dataset
    if id == 0:
        return pd.read_csv(path.joinpath('movies.dat'), sep='::', engine='python', header=None, names=movie_header)
    elif id == 1:
        return pd.read_csv(path.joinpath('ratings.dat'), sep='::', engine='python', header=None, names=ratings_header)
    elif id == 2:
        return pd.read_csv(path.joinpath('users.dat'), sep='::', engine='python', header=None, names=user_header)
    elif id == 3:
        return pd.read_csv(path.joinpath('movies_metadata.csv'), engine='python')
    else:
        return


moviesDf = pd.DataFrame(get_data(0))
ratingsDf = pd.DataFrame(get_data(1))
usersDf = pd.DataFrame(get_data(2))
metaDf = pd.DataFrame(get_data(3))
metaDf = metaDf.rename(columns={"id": movie_header[0], "title": movie_header[1]})
metaDf = metaDf[metaDf[movie_header[0]].apply(lambda x: str(x).isdigit())]
metaDf[movie_header[0]] = metaDf[movie_header[0]].astype(int)


def find_movie(movie_name):
    movies = moviesDf[moviesDf[movie_header[1]].str.contains(movie_name, regex=True, flags=re.IGNORECASE)]
    return movies


def movie_json(movie_name):
    searched_movies = find_movie(movie_name=movie_name)

    searched_movies[movie_header[2]] = searched_movies[movie_header[2]].str.replace("|", ',')
    searched_movies[movie_header[1]] = searched_movies[movie_header[1]].str.replace("[^a-zA-Z\s]","")
    print(searched_movies)
    movie_meta = pd.merge(searched_movies, metaDf, on='Title', how="left")
    json_movies = movie_meta.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_movies)
    movies_context = {'d': data}
    return movies_context


if __name__ == '__main__':
    movie_json("Hello")
