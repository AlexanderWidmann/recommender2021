import pandas as pd
import numpy

def to_float(x):
    try:
        x = float(x)
    except:
        x = numpy.nan
    return x


if __name__ == '__main__':
    df = pd.read_csv("../movies_metadata.csv", low_memory=False)
    print(df.tail(1).values)
    print(df.head(1).values)

    getJumanji = df.loc[df['original_title'] == "Jumanji"]

    print (getJumanji.values)


    small_df = df[['title', 'release_date', 'popularity', 'revenue', 'runtime',
    'genres']].copy()
    small_df.loc['release_date'] = pd.to_datetime(small_df['release_date'],
    errors='coerce')
    small_df['release_year'] = small_df['release_date'].apply(lambda x: str(x).split('-')[0] if x != numpy.nan else numpy.nan)
    small_df['release_year'] = small_df['release_year'].apply(to_float)
    small_df['release_year'] = small_df['release_year'].astype('float')
    small_df = small_df.drop(columns="release_date")

    youngMovies = small_df[small_df['release_year'] >= 2010]
    print(youngMovies)

