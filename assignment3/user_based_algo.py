import pandas as pd


def computeUserBased(userid, path):
    moviesDf = pd.DataFrame(getData(path)[0])
    ratingsDf = pd.DataFrame(getData(path)[1])
    usersDf = pd.DataFrame(getData(path)[2])

    #First inner join with the ratings, then innerJoin with movies (n:n Relationship)

    joined = usersDf.merge(ratingsDf, how='inner', on='user_id')

    joinMovieUser = joined.merge(moviesDf, how='inner', on='movie_id')

    ###SHOW FIRST 15 MOVIES + GENRES WITH WERE RATED BY THE GIVEN USER

    showFirstFifteenMovies(joinMovieUser, userid)



def showFirstFifteenMovies(movies, userid):

    #Select the movies which where rated by the given user
    #In SQL it would be SELECT * where user_id = x
     userMovies = movies[movies["user_id"] == userid]

     print (userMovies[["movie","genres"]].head(15))


def getData(path):
    movies = pd.read_csv(path + "movies.csv")
    ratings = pd.read_csv(path + "ratings.csv")
    users = pd.read_csv(path + "users.csv")

    return movies, ratings, users


if __name__ == '__main__':
    print("Please enter the UserId: ")

    userid = int( input())

    computeUserBased(userid, "./MovieLens_1M/")
