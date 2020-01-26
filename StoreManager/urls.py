from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index),
    path('rayon', views.rayon),
    path(r'connexion', views.connexion, name='connexion'),
    path(r'deconnexion', views.deconnexion, name='deconnexion'),
]