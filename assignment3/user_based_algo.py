import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 1000)
path = "./MovieLens_1M/"

# dataset is pulled from:
# https://grouplens.org/datasets/movielens/1m/
# contains 4 files: movies.dat, ratings.dat, README and users.dat
# the data contains no header and is separated by '::', header-information can be found in the readme
# the headers are also used to access the columns to avoid errors caused by typos
movie_header = ['MovieId', 'Title', 'Genre']
ratings_header = ['UserId', 'MovieId', 'Ratings', 'Timestamp']
user_header = ['UserId', 'Gender', 'Age', 'Occupation', 'ZipCode']

# correlation-methods:
# 0 for pearson (since this can not be used alone (too small sample set sometimes contains only
# the same ratings for the movies) rest for spearman
correlation_method = 1

# custom headers (for the DF where the neighbors are stored
neighbors_header = ['UserId', 'Similarity']
neighbors_helper_header = ['RatingSim', 'Overlap']
neighbors_rated_header = ['MovieId', 'ScoredRating']

# other metadata (like neighborhood_size and min overlap)
movie_amount = 10
neighborhood_size = 20
min_overlap = 3
min_rating = 3


# Loads the Data
# 1 for movies, 2 for ratings and 3 for users
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


# get the user input
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


# calculate the pearson correlation
# based on: https://www.statisticshowto.com/probability-and-statistics/correlation-coefficient-formula/spearman-rank-correlation-definition-calculate/
def get_spearman_corr(ratings):
    # get the difference and then square it
    ratings['d2'] = (ratings['Ratings_x'] - ratings['Ratings_y']) ** 2
    n = len(ratings)
    dividend = 6 * sum(ratings['d2'])
    divisor = n * (n ** 2 - 1)
    # spearman formula:  1 - (6 * Summe ((Unterschied x -y)²)) / (n* ( n² -1)
    result = 1 - dividend / divisor
    if result < 0:
        return 0
    return result


# calculate the pearson correlation ( perhaps not the best method since it can not be standalone)
# based on: https://www.statisticshowto.com/probability-and-statistics/correlation-coefficient-formula/
def get_pearson_corr(ratings):
    ratings['xy'] = ratings['Ratings_x'] * ratings['Ratings_y']
    ratings['x2'] = ratings['Ratings_x'] ** 2
    ratings['y2'] = ratings['Ratings_y'] ** 2
    # helper variable for the length of the array
    n = len(ratings)
    # helper variables to calculate the sum for the columns
    xy = sum(ratings['xy'])
    x = sum(ratings['Ratings_x'])
    y = sum(ratings['Ratings_y'])
    x2 = sum(ratings['x2'])
    y2 = sum(ratings['y2'])
    # n*(Summe(x*y) - (Summe(x) * Summe(y))
    dividend = n * xy - x * y
    # Square root ((n* Summe(x²) - Summe(x)²) * (n* Summe(y²) - Summe(y)²))
    divisor = ((n * x2 - x ** 2) * (n * y2 - y ** 2)) ** (1 / 2)
    # if the divisor is 0, spearman does not work for this dataset, so we use the spearman method
    if divisor == 0:
        return get_spearman_corr(ratings)
    result = dividend / divisor
    if result < 0:
        return 0
    return result


def calc_similarity_and_overlap_percentage(current_user, selected_user):
    # intersect (we only need to  evaluate movies both rated directly, overlap count affects the outcome differently
    merged_ratings = pd.merge(current_user[[movie_header[0], ratings_header[2]]],
                              selected_user[[movie_header[0], ratings_header[2]]], how='inner', on=movie_header[0])
    movie_overlap = merged_ratings[movie_header[0]].nunique()
    # minimum overlap is required to consider the user
    if movie_overlap < min_overlap:
        return [0, 0]
    # use the correlation method pearson to calculate the correlation between the users
    if correlation_method == 0:
        similarity = get_pearson_corr(merged_ratings[['Ratings_x', 'Ratings_y']])
    else:
        similarity = get_spearman_corr(merged_ratings[['Ratings_x', 'Ratings_y']])
    # create the proper result element
    result = [
        similarity,
        movie_overlap / len(selected_user.index)
    ]
    return result


# method to get the nearest neighbors
# neighborhood_size: amount of neighbors returned
def get_nearest_neighbors(userid):
    # group the ratings by userid
    ratings_grouped = ratingsDf.groupby(user_header[0])
    # get the selected user
    selected_user = ratings_grouped.get_group(userid)
    # helper array to easier calculate the nearest neighbor
    user_helper = []

    # iterate the groups
    for current_user_id, current_user in ratings_grouped:
        # skip if the user is the selected user
        if current_user_id == userid:
            continue

        # calculate the similarity
        sim = calc_similarity_and_overlap_percentage(current_user, selected_user)
        # add the user to the df
        user_helper += [{
            neighbors_header[0]: current_user_id,
            neighbors_helper_header[0]: sim[0],
            neighbors_helper_header[1]: sim[1]
        }]

    result = pd.DataFrame(user_helper)
    # only use the relative overlap (compared to the maximum occurring overlap) to create easier to read numbers
    result[neighbors_helper_header[1]] = result[neighbors_helper_header[1]].div(
        result[neighbors_helper_header[1]].max())
    # calculate the final relevance score by multiplying the pearson correlation and the relative overlap
    result[neighbors_header[1]] = result[neighbors_helper_header[0]] * result[neighbors_helper_header[1]]
    # sort the dataframe (biggest first) and return the number of neighbors defined in the neighborhood_size
    return result.nlargest(neighborhood_size, neighbors_header[1])[neighbors_header]


# recommend movies based on the nearest neighbors
def knn_recommend_movies(userid):
    neighbors = get_nearest_neighbors(userid)
    # add the ratings
    neighbors_with_ratings = pd.merge(ratingsDf[[ratings_header[0], ratings_header[1], ratings_header[2]]],
                                      neighbors[neighbors_header], on=user_header[0])
    # query to get the movies the current user watched
    current_movies = ratingsDf.query('UserId==' + str(userid))[movie_header[0]]
    neighbors_with_ratings = neighbors_with_ratings.query('MovieId not in @current_movies')
    # filter out badly rated movies (average in the "neighborhood")
    bad_avg_ratings = neighbors_with_ratings.groupby(movie_header[0]).agg('mean')
    bad_avg_ratings = bad_avg_ratings[bad_avg_ratings[ratings_header[2]] < min_rating]
    neighbors_with_ratings = neighbors_with_ratings.query('MovieId not in @bad_avg_ratings')
    # apply the relevance based on the similarity
    neighbors_with_ratings[neighbors_rated_header[1]] = neighbors_with_ratings[ratings_header[2]] * \
                                                        neighbors_with_ratings[neighbors_header[1]]
    # keep only the relevant columns (MovieId and the weighted rating
    movies_avg_rating = neighbors_with_ratings[neighbors_rated_header].groupby(movie_header[0], as_index=False).agg(
        'mean')
    # get the ids of the best rated movies by the neighbors
    chosen_movies = movies_avg_rating.nlargest(movie_amount, neighbors_rated_header[1])[movie_header[0]]
    return moviesDf.query('MovieId in @chosen_movies')


if __name__ == '__main__':
    # initialize the data
    moviesDf = pd.DataFrame(get_data(0))
    ratingsDf = pd.DataFrame(get_data(1))
    usersDf = pd.DataFrame(get_data(2))

    userid = get_user_id()

    # print the first 15 movies for the selected user
    show_first_fifteen_movies(userid)

    print(knn_recommend_movies(userid).to_string(index=False))
