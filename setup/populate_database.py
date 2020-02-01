import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django

django.setup()

from django.contrib.auth.models import User
from StoreManager.models import Employee, Department, Store, Product

class PopulateDatabase:
    def start(self):
        self.create_super_user()
        self.create_store()
        self.create_departement()
        self.create_user()
        self.create_product()

    def create_super_user(self):
        self.superuser = User.objects.create_superuser("admin", "fakemail2@mail.com", "admin")
        self.superuser.save()

    def create_store(self):
        self.store = Store(name="store", user=self.superuser)
        self.store.save()

    def create_departement(self):
        self.department_foot = Department(name="Football", store=self.store)
        self.department_foot.save()

        self.department_tennis = Department(name="Tennis", store=self.store)
        self.department_tennis.save()

        self.department_running = Department(name="Running", store=self.store)
        self.department_running.save()

    def create_user(self):
        self.user1 = User.objects.create_user("Michel", "michel@mail.com", "password")
        self.user1.save()
        self.employee1 = Employee(user=self.user1, phonenumber="0505050505", department=self.department_foot)
        self.employee1.save()

        self.user2 = User.objects.create_user("Jean", "jean@mail.com", "password")
        self.user2.save()
        self.employee2 = Employee(user=self.user2, phonenumber="0505050505", department=self.department_tennis)
        self.employee2.save()

        self.user3 = User.objects.create_user("Alberto", "alberto@mail.com", "password")
        self.user3.save()
        self.employee3 = Employee(user=self.user3, phonenumber="0505050505", department=self.department_running)
        self.employee3.save()

    def create_product(self):
        self.product1 = Product(name="Ballon low", quantity=78, ref="B1", price=25.0,
                                department_id=self.department_foot.id)
        self.product2 = Product(name="Ballon medium", quantity=456, ref="B2", price=50.0,
                                department_id=self.department_foot.id)
        self.product3 = Product(name="Ballon high", quantity=1025, ref="B3", price=99.0,
                                department_id=self.department_foot.id)
        self.product4 = Product(name="Raquette low", quantity=55, ref="T1", price=18.0,
                                department_id=self.department_tennis.id)
        self.product5 = Product(name="Raquette medium", quantity=789, ref="T2", price=45.0,
                                department_id=self.department_tennis.id)
        self.product6 = Product(name="Raquette high", quantity=999, ref="T3", price=150.0,
                                department_id=self.department_tennis.id)

        self.product7 = Product(name="Chaussure low", quantity=66, ref="C1", price=32.0,
                                department_id=self.department_running.id)
        self.product8 = Product(name="Chaussure medium", quantity=666, ref="C2", price=56.0,
                                department_id=self.department_running.id)
        self.product9 = Product(name="Chaussure high", quantity=6666, ref="C3", price=124.0,
                                department_id=self.department_running.id)

        self.product1.save()
        self.product2.save()
        self.product3.save()
        self.product4.save()
        self.product5.save()
        self.product6.save()
        self.product7.save()
        self.product8.save()
        self.product9.save()


if __name__ == '__main__':
    print("Création des données")
    populate_database = PopulateDatabase()
    populate_database.start()
    print("Données créées")
