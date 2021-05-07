import time

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

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

# helper header for the evaluation

evaluation_header = ['RelevanceRating', 'RelevanceScore']

# other metadata (like neighborhood_size and min overlap)
movie_amount = 10
neighborhood_size = 20  # default 20
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
    ratings_grouped = train_ratings.groupby(user_header[0])
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
    # calculate the final relevance score by multiplying the pearson correlation and the relative overlap
    result[neighbors_header[1]] = result[neighbors_helper_header[0]] * result[neighbors_helper_header[1]]
    # sort the dataframe (biggest first) and return the number of neighbors defined in the neighborhood_size

    return result.nlargest(neighborhood_size, neighbors_header[1])[neighbors_header]


# recommend movies based on the nearest neighbors
def knn_recommend_movies(userid):
    neighbors = get_nearest_neighbors(userid)
    # add the ratings
    neighbors_with_ratings = pd.merge(test_ratings[[ratings_header[0], ratings_header[1], ratings_header[2]]],
                                      neighbors[neighbors_header], on=user_header[0], how="inner")
    # query to get the movies the current user watched
    current_movies = test_ratings.query('UserId==' + str(userid))[movie_header[0]]
    # neighbors_with_ratings = neighbors_with_ratings.query('MovieId not in @current_movies')
    # filter out badly rated movies (average in the "neighborhood")
    bad_avg_ratings = neighbors_with_ratings.groupby(movie_header[0]).agg('mean')
    bad_avg_ratings = bad_avg_ratings[bad_avg_ratings[ratings_header[2]] < min_rating]
    neighbors_with_ratings = neighbors_with_ratings.query('MovieId not in @bad_avg_ratings')
    # apply the relevance based on the similarity
    neighbors_with_ratings[neighbors_rated_header[1]] = neighbors_with_ratings[ratings_header[2]] * \
                                                        neighbors_with_ratings[neighbors_header[1]]
    # keep only the relevant columns (MovieId and the weighted rating
    # movies_avg_rating = neighbors_with_ratings[neighbors_rated_header].groupby(movie_header[0], as_index=False).agg(
    #  'mean')
    # get the ids of the best rated movies by the neighbors
    # chosen_movies = movies_avg_rating.nlargest(movie_amount, neighbors_rated_header[1])[movie_header[0]]

    # weight the score relative to the maximum relevance score
    neighbors_with_ratings[neighbors_rated_header[1]] =neighbors_with_ratings[neighbors_rated_header[1]].div(
        neighbors_with_ratings[neighbors_rated_header[1]])
    #  get a relative rating for the recommended movies (rating will fluctuate between 3 and 5
    # -> since the user should at least find the recommended move average)
    neighbors_with_ratings[neighbors_rated_header[1]] = neighbors_with_ratings[neighbors_rated_header[1]] * 2 + 3

    return neighbors_with_ratings


def split_datasets(df):
    train, test = train_test_split(df, test_size=0.2)
    return train, test


def compute_MAE(df):
    df['diff'] = np.abs(df['ScoredRating'] - df['Ratings'])
    mae = df['diff'].sum()
    mae = mae * (1 / (df.size))

    return mae


def compute_RMSE(df):
    df['diff'] = (df['Ratings'] - df['ScoredRating']) ** 2

    rmse = df['diff'].sum()
    rmse = rmse * (1 / (df.size))

    rmse = np.sqrt(rmse)

    return rmse


# computes the matrix for each user-item pair.
def compute_user_item_matrix():
    scored_df = pd.DataFrame(columns=["UserId", "MovieId", "Ratings", "Similarity", "ScoredRating"])

    test_users_id = test_ratings['UserId'].unique()

    # compute the values for every user in the test set
    for user_id in test_users_id:
        scored_df = scored_df.append(knn_recommend_movies(user_id), ignore_index=True)
    return scored_df


def compute_precision_recall(df):
    # This line calculates the relevance for the ratings and the predicted ratings
    # It has been implemented this way for illustration purposes, lambda function looks better
    # True = positive and False = negative
    df.loc[df['Ratings'] >= 3, evaluation_header[0]] = True
    df.loc[df['Ratings'] < 3, evaluation_header[0]] = False
    df.loc[df['ScoredRating'] >= 3, evaluation_header[1]] = True
    df.loc[df['ScoredRating'] < 3, evaluation_header[1]] = False

    # determine True Positive
    df["TP"] = df.apply(helperTruePositv, axis=1)
    # determine False Positive
    df["FP"] = df.apply(helperFalsePositiv, axis=1)
    # determine False Negative
    df["FN"] = df.apply(helperFalseNegativ, axis=1)

    # calculates the sum for each type, to calculate precision and recall
    true_positves = df['TP'].sum()
    false_positives = df['FP'].sum()
    false_negative = df['FN'].sum()
    # calculates precision and recall based on the formula from the slides
    precision = true_positves / (true_positves + false_positives)
    recall = true_positves / (true_positves + false_negative)

    return precision, recall


# helper method to determine if True Positive or not
def helperTruePositv(x):
    if x[evaluation_header[0]] and x[evaluation_header[1]]:
        return 1
    else:
        return 0


# helper method to determine if False Positive or not
def helperFalsePositiv(x):
    if (x[evaluation_header[0]] == False) and (x[evaluation_header[1]]):
        return 1
    else:
        return 0


# helper method to determine if False Negative or not
def helperFalseNegativ(x):
    if (x[evaluation_header[0]]) and (x[evaluation_header[1]] == False):
        return 1
    else:
        return 0


if __name__ == '__main__':
    # Measures the time to get an idea of how long the calculation took
    curTime = time.time()

    # initialize the data
    moviesDf = pd.DataFrame(get_data(0))
    ratingsDf = pd.DataFrame(get_data(1).head(10000))
    usersDf = pd.DataFrame(get_data(2))

    # Split the dataset
    train_ratings, test_ratings = split_datasets(ratingsDf)

    # get the user-item matrix
    scored_df = compute_user_item_matrix()
    # to replay NaN values with 0 (to prevent errors in the calculation)
    scored_df.fillna(0, inplace=True)
    # compute the evaluation metrics
    MAE = compute_MAE(scored_df)
    RMSE = compute_RMSE(scored_df)
    precision, recall = compute_precision_recall(scored_df)

    # print the values
    print("MAE: ", MAE)
    print("RMSE: ", RMSE)
    print("Precision: ", precision)
    print("Recall: ", recall)

    # also print the needed time
    print("Time needed for calculation: ", time.time() - curTime)
