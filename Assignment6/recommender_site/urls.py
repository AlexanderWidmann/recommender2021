from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path ('get_id', views.get_id, name ='get´_id'),

]