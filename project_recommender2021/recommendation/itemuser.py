import __init__ as it
import pandas as pd

data = it.getData()

moviesDf = data[0]
ratingsDf = data[1]
genome_scoresDf = data[2]
genome_tagsDf = data[3]
tags_Df = data[4]
movies_metaDataDf = data[5]


def algo(id):
    # Get All Users who has rated the  movie with the given id

    movies_ratings = pd.merge(ratingsDf, moviesDf)

    movies_ratings_pivot = movies_ratings.pivot_table(index="userId", columns="movieId", values="rating", fill_value=0)
    # movies_ratings_pivot.fillna(0)

    ratings_movie = movies_ratings_pivot[id]
    # print(ratings_movie)
    similiar_movies = movies_ratings_pivot.corrwith(ratings_movie)

    similiar_movies.dropna(inplace=True)
    similiar_movies = pd.DataFrame({"movieId": similiar_movies.index, "correlation": similiar_movies.values})
    similiar_movies.drop(0, inplace=True)
    #similiar_movies.sort_values(by="correlation", ascending=False, inplace=True)

    similiar_movies = pd.merge(similiar_movies, movies_metaDataDf,left_on="movieId", right_on="MovieId", how="inner")
    similiar_movies.sort_values(by="correlation")

    return similiar_movies

if __name__ == '__main__':
    algo(1)
