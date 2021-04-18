import pandas as pd
import numpy as np


def computeUserBased(userid, path):
    moviesDf = pd.DataFrame(getData(path)[0])
    ratingsDf = pd.DataFrame(getData(path)[1])
    usersDf = pd.DataFrame(getData(path)[2])

    # First inner join with the ratings, then innerJoin with movies (n:n Relationship)

    joined = usersDf.merge(ratingsDf, how="inner", on='user_id')

    joinMovieUser = joined.merge(moviesDf, how="inner", on='movie_id')

    joinMovieUser = joinMovieUser.dropna()

    ###SHOW FIRST 15 MOVIES + GENRES WICH WERE RATED BY THE GIVEN USER

    # showFirstFifteenMovies(joinMovieUser, userid)

    calcSimilarity(joinMovieUser, userid)


def showFirstFifteenMovies(movies, userid):
    # Select the movies which where rated by the given user
    # In SQL it would be SELECT * where user_id = x
    userMovies = movies[movies["user_id"] == userid]

    print(userMovies[["movie", "genres"]].head(15))


def getData(path):
    movies = pd.read_csv(path + "movies.csv")
    ratings = pd.read_csv(path + "ratings.csv")
    users = pd.read_csv(path + "users.csv")

    return movies, ratings, users


def calcSimilarity(userDf, userid):
    simPivot = pd.pivot_table(userDf, index="user_id", columns=["movie_id"], values="rating")

    # get the user with the given userid
    # currentUser = userDf[userDf["user_id"] == userid]

    # calculate the mean for every user
    groupedMean = userDf.groupby('user_id')['rating'].mean()

    # add the mean to the dataframe
    joinMean = userDf.join(groupedMean, on="user_id", how="right", rsuffix="_mean")

    # calculate the adapted mean, with will used by the pearson correlation (basically r_a_p - ra_mean)
    joinMean['rating_adapted'] = joinMean['rating'] - joinMean['rating_mean']

    currentUser = joinMean.iloc[1]

    calculatePearsonSim(joinMean.head(1000), currentUser)

    print(joinMean.keys())


def calculatePearsonSim(df, user_id):
    df = pd.DataFrame(df)
    currentUser = getUserGroup(user_id=user_id, df=df)

    grouped = df.groupby('user_id')

    for name,group in grouped:

        print(calcSimilarityBetweenTwoUsers(user_1=currentUser, user_2=group))


def getUserGroup(user_id, df):
    user = df[df["user_id"] == 3]

    return user.groupby('user_id').get_group(
        3
    )


def calcSimilarityBetweenTwoUsers(user_1, user_2):

    user_1Df = pd.DataFrame(user_1)
    user_2_Df = pd.DataFrame(user_2)

    user_1Df = user_1Df.reset_index()
    user_2_Df = user_2_Df.reset_index()
    sim = 0
    if (user_1Df['user_id'][0] != user_2_Df['user_id'][0]):


        merged = pd.merge(user_1Df, user_2_Df, on=['movie_id'], how='inner')

        merged['numenator'] = merged['rating_adapted_x'] * merged['rating_adapted_y']
        numenator = merged['numenator'].sum()

        merged['denominator'] = np.sqrt(pow(merged['rating_adapted_x'], 2)) * np.sqrt(pow(merged['rating_adapted_y'], 2))
        denominator = merged['denominator'].sum()

        sim = numenator / denominator

    return sim


if __name__ == '__main__':
    print("Please enter the UserId: ")

    userid = int(input())

    computeUserBased(userid, "./MovieLens_1M/")
