# Task 2.2
import pandas as pd
import numpy as np

if __name__ == '__main__':
    data = [['Toy Story', 21.946943],
            ['Jumanji', 17.015539], ['Grumpier Old Men', 11.7129]]

    dFrame = pd.DataFrame(data, columns=['title', 'popularity'])
    dFrame = pd.DataFrame.sort_values(dFrame, by='popularity', ascending=True)

    print (dFrame.get("popularity"))


