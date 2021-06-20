import os, json
import pandas as pd
import glob

# based on: https://stackoverflow.com/questions/57067551/how-to-read-multiple-json-files-into-pandas-dataframe
# TO import all the json files in the extracted_jsons folder
relative_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_pattern = os.path.join(relative_path,'metadatageneration','extracted_jsons','*.json')
file_list = glob.glob(json_pattern)

meta_header = ['title', 'genres', 'runtime', 'directors', 'actors', 'languages', 'releaseDate', 'dvdReleaseDate', 'movieId', 'mpaa', 'imdbMovieId', 'originalTitle', 'youtubeTrailerIds', 'plotSummary', 'tmdbMovieId', 'avgRating', 'releaseYear', 'numRatings', 'posterPath',
               'tmdb-keywords', 'tmdb-production-companies', 'tmdb-budged', 'tmdb-revenue', 'tmdb-runtime', 'tmdb-vote-average', 'tmdb-collection-name',
               'imdb-country', 'imdb-reviews', 'imdb-production-companies']

def get_name_from_json(json_obj):
    name = json_obj['name']
    return name

# generate dataframe
df = pd.DataFrame(data=None, columns=meta_header)

for file in file_list:
    # read data frame from json file
    data = pd.read_json(file)
    # create a series with all the wanted information
    movielens = data['movielens'].dropna()

    if ('tmdb' in data):
        tmdb = data['tmdb']
        # adding values tmdb-values to the movielens metadata
        movielens['tmdb-keywords'] = list(map(get_name_from_json,tmdb['keywords']))
        movielens['tmdb-production-companies'] = list(map(get_name_from_json,tmdb['production_companies']))
        movielens['tmdb-budged'] = tmdb['budget']
        movielens['tmdb-revenue'] = tmdb['revenue']
        movielens['tmdb-runtime'] = tmdb['runtime']
        movielens['tmdb-vote-average'] = tmdb['vote_average']
        if(tmdb['belongs_to_collection'] is not None):
            movielens['tmdb-collection-name'] = map(get_name_from_json,tmdb['belongs_to_collection'])
        else:
            movielens['tmdb-collection-name'] = ''

    # adding values imdb-values to the movielens metadata
    if ('imdb' in data):
        imdb = data['imdb']
        movielens['imdb-country'] = imdb['country']
        movielens['imdb-reviews'] = imdb['reviews']
        movielens['imdb-production-companies'] = imdb['productionCompanies']

    df = df.append(pd.Series(data= movielens))

df = df.set_index('movieId')
# concatenate all the data frames in the list
df.to_csv('custom_metadata.csv', sep=',')
print(df)