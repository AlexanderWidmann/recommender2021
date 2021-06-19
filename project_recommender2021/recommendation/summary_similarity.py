from datetime import datetime
from pathlib import Path
from scipy.sparse import load_npz
import pandas as pd
import recommendation as rec

p = Path(__file__).parent
path = p.joinpath('ml-25m')

similarity = load_npz('ml-25m/similarity_matrix.npz')

def get_cosine_similarity(id):
    index = rec.getMoviesMeta().index.get_loc(id)
    # get similarities for this movie
    # use .toarray() to convert from sparse matrix
    # use [0] to convert "matrix" with only one row to one-dimensional array
    similarities = similarity[index].toarray()[0]
    return pd.Series(index=rec.getMoviesMeta().index, data=similarities[:rec.AmountRows]).drop(id)

