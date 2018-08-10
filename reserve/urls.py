from django.urls import path
from . import views

urlpatterns = [
    path('', views.reserve, name='reserve'),
    path('audience/', views.audience_form, name='audience_form'),
    path('artist/', views.artist_form, name='artist_form'),
]