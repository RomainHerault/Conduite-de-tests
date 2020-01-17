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

    user = models.OneToOneField(Employee, on_delete=models.CASCADE)


class Product(models.Model):
    quantity = models.IntegerField()
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    ref = models.CharField(max_length=150)

    department = models.ForeignKey('Department', on_delete=models.CASCADE)
