# Task 2.2
import pandas as pd
import numpy as np

if __name__ == '__main__':
    data = [['Toy Story', 21.946943],
            ['Jumanji', 17.015539], ['Grumpier Old Men', 11.7129]]

    #instance an new DataFrame with title and popularity as columns
    dFrame = pd.DataFrame(data, columns=['title', 'popularity'])
    #sort the values by popularity and ascending
    dFrame = pd.DataFrame.sort_values(dFrame, by='popularity', ascending=True)

    #print the popularity
    print (dFrame['popularity'])


