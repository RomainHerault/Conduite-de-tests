from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index),
    path(r'rayon', views.rayon, name='rayon'),
    path('departement', views.departement),
    path('employe', views.employe),
    path(r'connexion', views.connexion, name='connexion'),
    path(r'deconnexion', views.deconnexion, name='deconnexion'),
]