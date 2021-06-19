"""project_recommender2021 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from index import views as index_views
from movie import views as movie_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_views.index, name='home'),
    path('getMovies', index_views.getMovies, name='movies'),
    path('showMovie', movie_views.showMovie, name='showMovie'),
    path('showRecommendationTags', movie_views.showRecommendationTags, name="showRecommandationTags"),
    path('showRecommendationTagsPattern', movie_views.showRecommendationTagsPattern, name="showRecommandationTagsPattern"),
    path("showRecommendationActors", movie_views.showRecommendationActors, name="showRecommendationActors"),
    path("showRecommendationRatings", movie_views.showRecommendationRatings, name="showRecommendationRatings"),
    path("showRecommendationUserRatings", movie_views.showRecommendationUserRatings, name="showRecommendationUserRatings"),
    path("showRecommendationSummary", movie_views.showRecommendationSummary, name="showRecommendationSummary"),

    path("showComboRecommendationSimpleMetaMulti", movie_views.showComboRecommendationSimpleMetaMulti, name="showComboRecommendationSimpleMetaMulti"),
    path("showComboRecommendationSimpleMeta", movie_views.showComboRecommendationSimpleMeta, name="showComboRecommendationSimpleMeta"),
    path("showComboRecommendationAllUnweighted", movie_views.showComboRecommendationAllUnweighted, name="showComboRecommendationAllUnweighted"),
    path("showComboRecommendationWeighted", movie_views.showComboRecommendationWeighted, name="showComboRecommendationWeighted"),
    path("showComboRecommendationCustom", movie_views.showComboRecommendationCustom, name="showComboRecommendationCustom"),
    path("showComboRecommendationAllCustom", movie_views.showComboRecommendationAllCustom, name="showComboRecommendationAllCustom"),
]
