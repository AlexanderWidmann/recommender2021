# Task 2.1 Getting used to Series

import pandas as pd
import numpy as np

if __name__ == '__main__':
    data = ['Toy Story', 'Jumanji', 'Grumpier Old Men']

    series = pd.Series(data)

    # print first element
    print(series.head(1))
    # print first two elements
    print(series.head(2))
    # print last two elements
    print(series.tail(2))

    #instance a series wich get the data from above
    indexedSeries = pd.Series(data, index=['a', 'b', 'c'])
    #print value with the index b
    print(indexedSeries.get('b'))
