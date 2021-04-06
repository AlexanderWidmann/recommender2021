import pandas as pd

if __name__ == '__main__':

    df = pd.read_csv("../movies_metadata.csv",low_memory=False)
    print (df.get("overview")[0])
    print(df.get("overview")[len(df)-1])

    #Show the Infromation of Jumanji..

