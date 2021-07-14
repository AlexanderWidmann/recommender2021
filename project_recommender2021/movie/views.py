from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
import movie.forms as forms
import recommendation as rec
import helper as hp
from django.urls import reverse
from index.forms import MoviesForm


# Create your views here.
def showMovie(request):
    form = forms

    id = request.POST.get('id')
    print(rec.find_movie_by_id(id))
    df = rec.find_movie_by_id(id)
    form.title = df['title'].iloc[0]
    form.plotSummary = df['plotSummary'].iloc[0]
    form.releaseYear = df['releaseDate']
    form.directors = hp.toPlainString(df['directors'].iloc[0])
    form.actors = hp.toPlainString(df['actors'].iloc[0])
    print(hp.toPlainString(df["youtubeTrailerIds"].iloc[0]))
    form.youtubeTrailerIds = hp.convertToYoutubeId(df["youtubeTrailerIds"].iloc[0])
    form.movieId = id

    return render(request, "movie.html", {"form": form})


def showRecommendationTags(request):
    id = int(request.POST.get("id"))
    movies = rec.similarMovieKeywords_recommender(int(id))
    return render(request, "recommandation.html", movies)


def showRecommendationTagsPattern(request):
    id = int(request.POST.get("id"))
    movies = rec.similarMoviesPattern_recommender(int(id))
    return render(request, "recommandation.html", movies)


def showRecommendationActors(request):
    id = int(request.POST.get("id"))
    movies = rec.similarMovieActors_recommender(int(id))
    return render(request, "recommandation.html", movies)


def showRecommendationRatings(request):
    id = int(request.POST.get("id"))
    movies = rec.similarMovieRatings_recommender(int(id))
    return render(request, "recommandation.html", movies)


def showRecommendationUserRatings(request):
    id = int(request.POST.get("id"))
    movies = rec.similarMovieUserRatings_recommender(int(id))
    return render(request, "recommandation.html", movies)


def showRecommendationSummary(request):
    id = int(request.POST.get("id"))
    movies = rec.similarMovieSummary_recommender(int(id))
    return render(request, "recommandation.html", movies)


def showRecommendationGenrePopularity(request):
    id = int(request.POST.get("id"))
    movies = rec.genrePopularity_recommender(int(id))
    return render(request, "recommandation.html", movies)


def showComboRecommendationSimpleMetaMulti(request):
    id = int(request.POST.get("id"))
    movies = rec.simpleMetaMulitplicated_recommender(int(id))
    return render(request, "recommandation.html", movies)


def showComboRecommendationSimpleMeta(request):
    id = int(request.POST.get("id"))
    movies = rec.simpleMeta_recommender(int(id))
    return render(request, "recommandation.html", movies)


def showComboRecommendationAllUnweighted(request):
    id = int(request.POST.get("id"))
    movies = rec.allAlgorithmsWithOptionalFactors_recommender(int(id))
    return render(request, "recommandation.html", movies)


def showComboRecommendationWeighted(request):
    id = int(request.POST.get("id"))
    movies = rec.allAlgorithmsWithOptionalFactors_recommender(int(id), genre_factor=4, popularity_factor=3,
                                                              actors_factor=1,
                                                              directors_factor=1,
                                                              pattern_factor=0.2, keywords_factor=1, rating_factor=0.6,
                                                              summary_factor=0.7)
    return render(request, "recommandation.html", movies)


def showComboRecommendationCustom(request):
    id = int(request.POST.get("id"))
    movies = rec.allAlgorithmsWithOptionalFactors_recommender(int(id), genre_factor=3, popularity_factor=2,
                                                              actors_factor=1,
                                                              directors_factor=1,
                                                              pattern_factor=0.2, keywords_factor=2, rating_factor=2,
                                                              summary_factor=2)
    return render(request, "recommandation.html", movies)


def showComboRecommendationAllCustom(request):
    id = int(request.POST.get("id"))
    movies = rec.allAlgorithmsWithOptionalFactors_recommender(int(id), genre_factor=3, popularity_factor=2,
                                                              actors_factor=1,
                                                              directors_factor=1,
                                                              pattern_factor=0.5, keywords_factor=1.5, rating_factor=1,
                                                              summary_factor=2)
    return render(request, "recommandation.html", movies)
