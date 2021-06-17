from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import movie.forms as forms
import recommendation as rec
import helper as hp


# Create your views here.
def showMovie(request):
    form = forms

    id = request.POST.get('id')
    print(rec.find_movie_by_id(id))
    df = rec.find_movie_by_id(id)
    form.title = df['title'].iloc[0]
    form.plotSummary = df['plotSummary'].iloc[0]
    form.releaseYear = df['releaseDate']
    form.directors = hp.toString(df['directors'].iloc[0])
    form.actors = hp.toString(df['actors'].iloc[0])
    form.movieId = id

    return render(request, "movie.html", {"form": form})


def showRecommendationTags(request):
    id = request.POST.get("id")
    movies = rec.similiarMovieKeywords(id)
    return render(request, "recommandation.html", movies)


def showRecommendationActors(request):
    id = request.POST.get("id")
    movies = rec.similiarMovieActors(id)
    return render(request, "recommandation.html", movies)

def showRecommendationRatings(request):
    id = request.POST.get("id")
    movies = rec.similarMovieRatings(int(id))
    return render(request, "recommandation.html", movies)
