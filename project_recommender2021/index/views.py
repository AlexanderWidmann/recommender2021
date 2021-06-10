from django.shortcuts import render
from django import forms
import recommendation as rec
from index.forms import MoviesForm


# Create your views here.
def index(request):
    form = MoviesForm
    return render(request, "index.html", {'form': form})


def getMovies(request):
    if request.method == "POST":
        movie_name = request.POST['movie_name']
        movie = rec.movie_json(movie_name)

    return render(request, "overview_movies.html", movie)

