from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


# Create your views here.
from django.urls import reverse

from . import forms


def index(request):
    return HttpResponse("Coucou Djangooooooooooooooooo !")


def rayon(request):
    header = ['Nom', 'Prix','Quantité','Ref','Nom Rayon']
    produits = [['Fraise',40,45689,'4567','Muscu'],['Melon',40,4789,'KLM78','Tennis'],['Rat mort',41,78945454,'XXTY78','Football']]
    return render(request, 'StoreManager/base.html', {'username': 'Jean Michel', 'header': header, 'data': produits})


def connexion(request):
    error = False
    if request.method == "POST":
        form = forms.ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = forms.ConnexionForm()

    return render(request, 'StoreManager/login.html', locals())

def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))