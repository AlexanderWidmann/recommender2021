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

    indexedSeries = pd.Series(data, index=['a', 'b', 'c'])
    print(indexedSeries.get('b'))
