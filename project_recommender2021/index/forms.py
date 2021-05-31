from django import forms
from django.forms import ModelForm
from index.models import MovieName

import pandas as pd


class MoviesForm(ModelForm):
    movie_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Search ...", }
        )
    )
    class Meta:
        model = MovieName
        fields = ['movie_name']
