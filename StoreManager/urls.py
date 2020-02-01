from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index),
    path(r'produit', views.produit, name='produit'),
    path('rayon', views.rayon),
    path('employe', views.employe),
    path(r'connexion', views.connexion, name='connexion'),
    path(r'deconnexion', views.deconnexion, name='deconnexion'),
]