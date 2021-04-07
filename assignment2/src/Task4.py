import pandas as pd






def computeMeanAndAverage(route):
    d = pd.read_csv(route)

    d1 = d.groupby('movieId').rating.agg(['mean', 'median'])

    return d1


if __name__ == '__main__':
    print(computeMeanAndAverage("../ratings_small.csv"))
