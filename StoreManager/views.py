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
        new_product = Product(name="", quantity=0, ref="", price=0,
                              department_id=1)  # TODO dept id à modifier en fonction des droits du user
        new_product.save()
    elif request.method == 'POST' and request.POST.get(
            'modify_product'):  # check if post request comes from correct button

        selected_products_id = request.POST.getlist('action_product')

        id_products = list(Product.objects.values_list('id', flat=True))
        id_products.sort()

        name_products = request.POST.getlist('name_product')
        price_products = request.POST.getlist('price_product')
        quantity_products = request.POST.getlist('quantity_product')
        ref_products = request.POST.getlist('ref_product')

        for product_id in selected_products_id:

            product = Product.objects.get(pk = product_id)

            product.name = name_products[id_products.index(int(product_id))]
            product.price = price_products[id_products.index(int(product_id))]
            product.quantity = quantity_products[id_products.index(int(product_id))]
            product.ref = ref_products[id_products.index(int(product_id))]
            product.save()

    elif request.method == 'POST' and request.POST.get(
            'delete_product'):  # check if post request comes from correct button

        selected_products = request.POST.getlist('action_product')  # get id of selected products
        Product.objects.filter(id__in=selected_products).delete()  # delete selected product

    header = ['Action', 'Nom', 'Prix', 'Quantité', 'Ref', 'Nom Rayon']
    query_results = Product.objects.all()  # TODO à modifier en fonction des droits du user
    return render(request, 'StoreManager/base.html',
                  {'username': 'Jean Michel', 'header': header, 'data': query_results})


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
