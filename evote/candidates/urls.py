from django.urls import path
from .views import *
from . import views


urlpatterns=[
    path('show_candidate/',show_candidate,name='show_candidate'),
    path('show_voters/',views.show_voters ,name='show_voters'),
    path('show_election/',show_election),
    path('show_result',show_result),
    path('vote_candidate/<int:candidate_id>/', views.vote_candidate, name='vote_candidate'),
]