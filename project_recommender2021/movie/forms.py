from django import forms
from django.forms import ModelForm
from movie.models import MovieId

import pandas as pd


class IdForm(ModelForm):
    class Meta:
        model = MovieId
        fields = ['movieId']
