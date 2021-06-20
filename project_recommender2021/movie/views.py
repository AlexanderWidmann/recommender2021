from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import movie.forms as forms
import recommendation as rec
import helper as hp


# Create your views here.
def showMovie(request):
    form = forms
    try:
        id = request.POST.get('id')
        print(rec.find_movie_by_id(id))
        df = rec.find_movie_by_id(id)
        form.title = df['title'].values[0]
        form.plotSummary = df['plotSummary'].values[0]
        form.releaseYear = df['releaseDate'].values[0]
        form.directors = hp.toString(df['directors'].values[0])
        form.actors = hp.toString(df['actors'].values[0])
        form.movieId = id
    except:
        return (render(request, "error.html"))
    finally:
        return render(request, "movie.html", {"form": form})


def showRecommendationTags(request):
    id = request.POST.get("id")
    try:
        movies = rec.similiarMovieKeywords(id)
    except:
        return (render(request, "error.html"))
    finally:
        return render(request, "recommandation.html", movies)


def showRecommendationActors(request):
    id = request.POST.get("id")
    try:
        movies = rec.similiarMovieActors(id)
    except:
        return (render(request, "error.html"))
    finally:
        return render(request, "recommandation.html", movies)


def showRecommendationRatings(request):
    id = request.POST.get("id")
    try:
        movies = rec.similarMovieRatings(int(id))
    except:
        return (render(request, "error.html"))
    finally:
        return render(request, "recommandation.html", movies)
