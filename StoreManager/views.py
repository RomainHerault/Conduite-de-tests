from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.urls import reverse

from StoreManager.models import Product
from . import forms


def index(request):
    return HttpResponse("Coucou Djangooooooooooooooooo !")


def rayon(request):
    if request.method == 'POST' and request.POST.get('add_product'):  # check if post request comes from correct button
        selected_products = request.POST.getlist('action_product')  # get id of selected products
    elif request.method == 'POST' and request.POST.get('modify_product'):  # check if post request comes from correct button
        selected_products = request.POST.getlist('name_product')  # get id of selected products
        print(selected_products)
    elif request.method == 'POST' and request.POST.get('delete_product'):  # check if post request comes from correct button
        selected_products = request.POST.getlist('action_product')  # get id of selected products
        Product.objects.filter(id__in=selected_products).delete()  # delete selected product

    header = ['Action', 'Nom', 'Prix', 'Quantité', 'Ref', 'Nom Rayon']
    query_results = Product.objects.all()  # TODO à modifier en fonction des droits du user
    return render(request, 'StoreManager/base.html',{'username': 'Jean Michel', 'header': header, 'data': query_results})




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
            else:  # sinon une erreur sera affichée
                error = True
    else:
        form = forms.ConnexionForm()

    return render(request, 'StoreManager/login.html', locals())


def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))
