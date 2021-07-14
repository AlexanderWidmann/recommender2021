
import pandas as pd

#calculates similiarity based on ratings
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
    similiar_movies = similiar_movies.dropna()
    # Cast to DataFrame
    similiar_movies = pd.DataFrame({"movieId": similiar_movies.index, "similarity": similiar_movies.values})

    # Merge with MetaDataDf to get Information like Overview etc.
    merged_movies = pd.merge(movies_metaDataDf, similiar_movies, right_on="movieId", left_on="MovieId", how="inner")
    print(list(movies_metaDataDf.columns))
    print(similiar_movies)
    print(merged_movies['similarity'])

    return merged_movies['similarity']

