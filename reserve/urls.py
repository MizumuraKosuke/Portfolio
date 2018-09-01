from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.reserve, name='reserve'),
    path('audience/', views.audience, name='audience'),
    path('live/<int:pk>', views.live_detail, name='live_detail'),
    path('live/<int:pk>/reserve', views.live_reserve, name='live_reserve'),
    path('reserve_form/', views.reserve_form, name='reserve_form'),
    path('create_live/', views.create_live, name='create_live'),
    path('create_artist/', views.create_artist, name='create_artist'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('create_done/', views.CreateDoneView.as_view(), name='create_done'),
    path('create_complete/<uidb64>/', views.CreateCompleteView.as_view(), name='create_complete')
]