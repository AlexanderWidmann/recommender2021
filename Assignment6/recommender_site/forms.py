from django import forms
from django.forms import ModelForm

import user_based_algo as cf
import pandas as pd

from recommender_site.models import UserId


class UserForm (ModelForm):
    class Meta:
        model = UserId
        fields = ['user_id']



