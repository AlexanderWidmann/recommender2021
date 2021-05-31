import pandas as pd
meta_header = ['title', 'genres', 'runtime', 'directors', 'actors', 'languages', 'releaseDate', 'dvdReleaseDate', 'movieId', 'mpaa', 'imdbMovieId', 'originalTitle', 'youtubeTrailerIds', 'plotSummary', 'tmdbMovieId', 'avgRating', 'releaseYear', 'numRatings', 'posterPath', 'tmdb-keywords',
               'tmdb-keywords', 'tmdb-production-companies', 'tmdb-budged', 'tmdb-revenue', 'tmdb-runtime', 'tmdb-vote-average', 'tmdb-collection-name',
               'imdb-country', 'imdb-reviews', 'imdb-production-companies']

df = pd.read_csv(('custom_metadata.csv'), sep=',', engine='python')

print(df.loc[6])
print(df.loc[7])
print(df.loc[8])
print(df.loc[9])
print(df.loc[10])