import nltk, string
from scipy.sparse import save_npz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import pandas as pd

meta_header = ['title', 'genres', 'runtime', 'directors', 'actors', 'languages', 'releaseDate', 'dvdReleaseDate', 'movieId', 'mpaa', 'imdbMovieId', 'originalTitle', 'youtubeTrailerIds', 'plotSummary', 'tmdbMovieId', 'avgRating', 'releaseYear', 'numRatings', 'posterPath',
               'tmdb-keywords', 'tmdb-production-companies', 'tmdb-budged', 'tmdb-revenue', 'tmdb-runtime', 'tmdb-vote-average', 'tmdb-collection-name',
               'imdb-country', 'imdb-reviews', 'imdb-production-companies']

# This class is used to pre-generate the cosine similarity for the movie-plotDescription
nltk.download('punkt')  # if necessary...
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

p = Path(__file__).parent
path = p.joinpath('ml-25m')


# remove punctuation and make all lowercase
def normalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punctuation_map))


# create the vecotorizer that and tokenizes the summary
vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')


def preprocess(summarySeries):
    tfidfMatrix = vectorizer.fit_transform(summarySeries.fillna(''))
    return cosine_similarity(tfidfMatrix, tfidfMatrix, dense_output=False)


def generate_similarity():
    metadata = pd.read_csv(path.joinpath('custom_metadata.csv'), engine="python")
    # store the matrix
    save_npz('ml-25m/similarity_matrix.npz', preprocess(metadata['plotSummary']))

if __name__ == '__main__':
    generate_similarity()
