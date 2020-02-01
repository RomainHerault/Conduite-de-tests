from django.db import models
from enum import Enum
from django.contrib.auth.models import User


# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.IntegerField()
    department = models.ForeignKey('Department', null=None, on_delete=models.CASCADE)


class Department(models.Model):
    name = models.CharField(max_length=150)

    store = models.ForeignKey('Store', on_delete=models.CASCADE)


class Store(models.Model):
    name = models.CharField(max_length=150)

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Product(models.Model):
    quantity = models.IntegerField()
    name = models.CharField(max_length=150)
    price = models.FloatField()
    ref = models.CharField(max_length=150)

    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    def isNotValid(self):
        try :
            self.quantity = int(self.quantity)
        except:
            return True,"Quantité invalide"
        try:
            self.quantity = float(self.quantity)
        except:
            return True,"Prix invalide"
        if self.name is "":
            return True,"Nom vide"
        if self.ref is "":
            return True,"Référence vide"
        return False,"OK"

    def doesRefExists(self):
        sameRefproducts = Product.objects.filter(ref = self.ref)
        if len(sameRefproducts) is not 0:
            if len(sameRefproducts) is not 1:
                return True, "Référence déjà existante"
            else:
                if sameRefproducts[0].id is not self.id :
                    return True, "Référence déjà existante"
        return False,"OK"