import __init__ as it
import pandas as pd
from scipy.spatial.distance import cosine
data = it.getData()

moviesDf = data[0]
ratingsDf = data[1]
genome_scoresDf = data[2]
genome_tagsDf = data[3]
tags_Df = data[4]
movies_metaDataDf = data[5]


def algo(id):
    # Get All Users who has rated the  movie with the given id
    allUsers = ratingsDf[ratingsDf["movieId"] == id]
    # Get all the other movies which were rated by the users
    print(allUsers)
    allRatings = ratingsDf[ratingsDf["userId"].isin(allUsers["userId"])]
    # print(allRatings)

    allMovies = ratingsDf[ratingsDf["movieId"].isin(allRatings["movieId"])]






if __name__ == '__main__':
    algo(1)
