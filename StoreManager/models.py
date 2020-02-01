from django.db import models
from enum import Enum
from django.contrib.auth.models import User


# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=20)
    department = models.ForeignKey('Department', null=None, on_delete=models.CASCADE)

    def doesNameExists(self):
        sameNameUser = User.objects.filter(username=self.user.username)
        if len(sameNameUser) is not 0:
            if len(sameNameUser) is not 1:
                return True, "nom d'utilisateur déjà existant"
            else:
                if sameNameUser[0].id is not self.user.id :
                    return True, "nom d'utilisateur déjà existant"
        return False,"OK"

class Department(models.Model):
    name = models.CharField(max_length=150)

    store = models.ForeignKey('Store', on_delete=models.CASCADE)

    def doesNameExists(self):
        sameNameDep = Department.objects.filter(name = self.name)
        if len(sameNameDep) is not 0:
            if len(sameNameDep) is not 1:
                return True, "département déjà existant"
            else:
                if sameNameDep[0].id is not self.id :
                    return True, "département déjà existant"
        return False,"OK"


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
        if self.quantity < 0:
            return True, "Quantité invalide"

        try:
            self.quantity = float(self.quantity)
        except:
            return True,"Prix invalide"

        if self.name is "":
            return True,"Nom vide"
        if self.ref is "":
            return True,"Reférence vide"
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