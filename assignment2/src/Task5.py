import pandas as pd


# get the similiar users
# Params:
# route: route to ratings dataset (default: 3)
# minSimiliarMovies: minimum amount of movie-overlap (default: 3)
def get_similar_users(route="../ratings_small.csv", user_id=1, min_similiar_movies=3):
    d = pd.read_csv(route, encoding='utf8', usecols=['userId', 'movieId', 'rating'])
    # group by user id
    d_grouped = d.groupby('userId')

    overlapping_users = []

    # get the first user (first group of the dataframe)
    target_movies = d_grouped.get_group(user_id)
    if target_movies.empty:
        return overlapping_users

    print('User ID: ' + (str)(user_id))
    print(target_movies[['movieId', 'rating']])

    # iterate the groups
    for current_user_id, movies in d_grouped:
        # skip if the user is the selected user
        if current_user_id == user_id:
            continue

        # using pd.merge to create the intersection (sql inner join per default == intersection)
        movie_intersection = pd.merge(movies, target_movies, on='movieId')
        # calculates number of unique movie overlap for the current user
        movie_overlap = movie_intersection['movieId'].nunique()

        # if overlap > minimum required add the user to the list
        if movie_overlap > min_similiar_movies:
            # remember userId, the overlap count, and the unique movieIds of the overlap
            overlapping_users += [{
                'userId': current_user_id,
                'overlapAmount': movie_overlap,
                'movieIds': movie_intersection.movieId.unique()
            }]

    # transform the list into a dataframe to make further manipulation/ access easier
    return pd.DataFrame(overlapping_users)


if __name__ == '__main__':
    # simple print ( could be adjusted to create a prettier/ more extensive print)
    print(get_similar_users())
