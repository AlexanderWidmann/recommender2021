import pandas as pd






def computeMeanAndAverage(route):
    d = pd.read_csv(route)
    #group by movie id and calculate mean and median by the agg function
    d1 = d.groupby('movieId').rating.agg(['mean', 'median'])

    return d1


if __name__ == '__main__':
    print(computeMeanAndAverage("../ratings_small.csv"))
