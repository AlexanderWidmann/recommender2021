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
    movies = rec.similarMovieKeywords_recommender(id)
    return render(request, "recommandation.html", movies)


def showRecommendationTagsPattern(request):
    id = request.POST.get("id")
    movies = rec.similarMoviesPattern_recommender(id)
    return render(request, "recommandation.html", movies)


def showRecommendationActors(request):
    id = request.POST.get("id")
    movies = rec.similarMovieActors_recommender(id)
    return render(request, "recommandation.html", movies)


def showRecommendationRatings(request):
    id = request.POST.get("id")
    movies = rec.similarMovieRatings_recommender(id)
    return render(request, "recommandation.html", movies)


def showRecommendationUserRatings(request):
    id = request.POST.get("id")
    movies = rec.similarMovieUserRatings_recommender(id)
    return render(request, "recommandation.html", movies)


def showRecommendationSummary(reqeuest):
    id = reqeuest.POST.get("id")
    movies = rec.similarMovieSummary_recommender(id)
    return render(reqeuest, "recommandation.html", movies)


def showComboRecommendationSimpleMetaMulti(reqeuest):
    id = reqeuest.POST.get("id")
    movies = rec.simpleMetaMulitplicated_recommender(id)
    return render(reqeuest, "recommandation.html", movies)


def showComboRecommendationSimpleMeta(reqeuest):
    id = reqeuest.POST.get("id")
    movies = rec.simpleMeta_recommender(id)
    return render(reqeuest, "recommandation.html", movies)


def showComboRecommendationAllUnweighted(reqeuest):
    id = reqeuest.POST.get("id")
    movies = rec.allAlgorithmsWithOptionalFactors_recommender(id)
    return render(reqeuest, "recommandation.html", movies)


def showComboRecommendationWeighted(reqeuest):
    id = reqeuest.POST.get("id")
    movies = rec.allAlgorithmsWithOptionalFactors_recommender(id, genre_factor=4, popularity_factor=3, actors_factor=1, directors_factor=1,
                                                              pattern_factor=0.2, keywords_factor=1, rating_factor=0.6, summary_factor=0.7)
    return render(reqeuest, "recommandation.html", movies)


def showComboRecommendationCustom(reqeuest):
    id = reqeuest.POST.get("id")
    movies = rec.allAlgorithmsWithOptionalFactors_recommender(id, genre_factor=3, popularity_factor=2, actors_factor=1, directors_factor=1,
                                                              pattern_factor=0.2, keywords_factor=0.6, rating_factor=0.6, summary_factor=1)
    return render(reqeuest, "recommandation.html", movies)


def showComboRecommendationAllCustom(reqeuest):
    id = reqeuest.POST.get("id")
    movies = rec.allAlgorithmsWithOptionalFactors_recommender(id, genre_factor=3, popularity_factor=2, actors_factor=1, directors_factor=1,
                                                              pattern_factor=0.5, keywords_factor=1.5, rating_factor=1, summary_factor=2)
    return render(reqeuest, "recommandation.html", movies)