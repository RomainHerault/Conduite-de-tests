from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Coucou Djangooooooooooooooooo !")

def rayon(request):
    header = ['Nom', 'Prix','Quantité','Ref','Nom Rayon']
    produits = [['Fraise',40,45689,'4567','Muscu'],['Melon',40,4789,'KLM78','Tennis'],['Rat mort',41,78945454,'XXTY78','Football']]
    return render(request, 'StoreManager/base.html', {'username': 'Jean Michel', 'header': header, 'data': produits})

