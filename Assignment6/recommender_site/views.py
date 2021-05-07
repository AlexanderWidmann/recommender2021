
from django.shortcuts import render


import user_based_algo as cf


from recommender_site.forms import UserForm


def index(request):
    #Get the UserForm which has the ids
    form = UserForm
    return render(request, "index.html", {'form': form})


def get_id(request):
    if request.method == "POST":
        #get the given id
        user_id = int(request.POST['user_id'])
        print(user_id)
        #get the recommended movies incl meta data  as json file
        movies = cf.get_recommended_movies_JSON(user_id)
    #return the recommendation.html which include the movies.
    return render(request, "recommendation.html", movies)
