import __init__ as it
import pandas as pd


def itemSimilarityRatings(id, data):

    moviesDf = data[0]
    ratingsDf = data[1]
    movies_metaDataDf = data[5]

    # Merge Movies with Ratings to get an Matrix
    movies_ratings = pd.merge(ratingsDf, moviesDf)
    # Create the pivot table / matrix
    movies_ratings_pivot = movies_ratings.pivot_table(index="userId", columns="movieId", values="rating", fill_value=0)

    # Get the Ratings from the selected Movie
    ratings_movie = movies_ratings_pivot[id]

    # Calculate the Similiarty between the Ratings-subsets
    similiar_movies = movies_ratings_pivot.corrwith(ratings_movie)

    # Drop NaN Values
    similiar_movies.dropna(inplace=True)
    # Cast to DataFrame
    similiar_movies = pd.DataFrame({"movieId": similiar_movies.index, "correlation": similiar_movies.values})

    # Merge with MetaDataDf to get Information like Overview etc.
    similiar_movies = pd.merge(similiar_movies, movies_metaDataDf, left_on="movieId", right_on="MovieId", how="inner")
    # Sort by correlation
    similiar_movies.sort_values(by="correlation", ascending=False, inplace=True)
    # Drop the first Movie (Corr = 1)
    similiar_movies.drop(0, inplace=True)
    return similiar_movies


if __name__ == '__main__':
    itemSimilarityRatings(1, it.getData())
