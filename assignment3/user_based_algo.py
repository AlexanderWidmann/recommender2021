import pandas as pd
import numpy as np


def computeUserBased(userid, path):
    moviesDf = pd.DataFrame(getData(path)[0])
    ratingsDf = pd.DataFrame(getData(path)[1])
    usersDf = pd.DataFrame(getData(path)[2])

    # First inner join with the ratings, then innerJoin with movies (n:n Relationship)

    joined = usersDf.merge(ratingsDf, how="inner", on='user_id')

    joinMovieUser = joined.merge(moviesDf, how="inner", on='movie_id')

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

    calculatePearsonSim(joinMean, currentUser)

    print(joinMean)


def calculatePearsonSim(df, currentUser):
    # COLUMNS FOR USER:
    # movie_id[0], age[1], job[2],user_id[3],zipcode[4], rating[5], timestamp[6], rating_mean[10], rating_adapted[11]
    users = df.values
    curUser = currentUser.values
    adj_curUser = curUser[11]

    matchCount = 0
    sim = pd.DataFrame(columns={"user_id", "sim"})

    for user in users:
        top = 0
        bot1 = 0
        bot2 = 0
        bottom = 0
        sim_ = 0
        adj_user = user[11]

        if user[0] == curUser[0]:
            top = top + (adj_user * adj_curUser)
            bot1 = bot1 + pow(adj_curUser,2)
            bot2 = bot2 + pow(adj_user,2)
            bottom = np.sqrt(bot1 * bot2)
            sim_0 = top / bottom
            print(sim_0)



if __name__ == '__main__':
    print("Please enter the UserId: ")

    userid = int(input())

    computeUserBased(userid, "./MovieLens_1M/")
