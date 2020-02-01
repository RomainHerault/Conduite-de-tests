from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from StoreManager.models import Employee, Department, Store, Product


class UnitTestsProduct(TestCase):
    department1 = None
    @classmethod
    def setUpTestData(cls):
        superuser = user = User.objects.create_superuser("superuser", "fakemail2@mail.com", "mdp")
        superuser.save()
        store = Store(name="store", user=superuser)
        store.save()
        cls.department1 = Department(name="d1", store=store)
        cls.department1.save()
    def test_isNotValid_correct(self):
        product = Product(quantity = 10, name = "Produit1", price = 10.2, ref = "Ref")
        result, error_msg = product.isNotValid()
        self.assertEqual(False, result)

    def test_isNotValid_quantity_neg(self):
        product = Product(quantity = -10, name = "Produit1", price = 10.2, ref = "Ref")
        result, error_msg = product.isNotValid()
        self.assertEqual(True, result)

    def test_isNotValid_quantity_string(self):
        product = Product(quantity = "coucou", name = "Produit1", price = 10.2, ref = "Ref")
        result, error_msg = product.isNotValid()
        self.assertEqual(True, result)

    def test_isNotValid_name_empty(self):
        product = Product(quantity = 10, name = "", price = 10.2, ref = "Ref")
        result, error_msg = product.isNotValid()
        self.assertEqual(True, result)

    def test_isNotValid_ref_empty(self):
        product = Product(quantity = 10, name = "Produit1", price = 10.2, ref = "")
        result, error_msg = product.isNotValid()
        self.assertEqual(True, result)

    def test_doesRefExists_correct(self):
        product = Product(quantity = 10, name = "Produit1", price = 10.2, ref = "Ref")
        result, error_msg = product.doesRefExists()
        self.assertEqual(False, result)

    def test_doesRefExists_incorrect(self):
        existing_product = Product(quantity=10, name="Produit1", price=10.2, ref="Ref", department = self.department1)
        existing_product.save()
        product = Product(quantity = 10, name = "Produit1", price = 10.2, ref = "Ref")
        result, error_msg = product.doesRefExists()
        self.assertEqual(True, result)

    def test_doesRefExists_correct_when_modify(self):
        existing_product = Product(quantity=10, name="Produit1", price=10.2, ref="Ref", department = self.department1)
        existing_product.save()
        existing_product.ref = "newRef"
        result, error_msg = existing_product.doesRefExists()
        self.assertEqual(False, result)


class UnitTestsEmployee(TestCase):
    username1 = "user1"
    password1 = "pass1"

    username2 = "user2"
    password2 = "pass2"

    super_username = "superuser"
    super_password = "superpass"

    employee2 = None

    department3 = None
    @classmethod
    def setUpTestData(cls):
        superuser = user = User.objects.create_superuser(cls.super_username, "fakemail2@mail.com", cls.super_password)
        superuser.save()
        store = Store(name="store", user=superuser)
        store.save()
        department1 = Department(name="d1", store=store)
        department1.save()
        department2 = Department(name="d2", store=store)
        department2.save()
        cls.department3 = Department(name="d3", store=store)
        cls.department3.save()
        user1 = User.objects.create_user(cls.username1, "fakemail@mail.com", cls.password1)
        user1.save()
        employee1 = Employee(user=user1, phonenumber="0505050505", department=department1)
        employee1.save()
        user2 = User.objects.create_user(cls.username2, "fakemail@mail.com", cls.password2)
        user2.save()
        cls.employee2 = Employee(user=user2, phonenumber="0505050506", department=department2)
        cls.employee2.save()

    def test_doesNameExists_correct(self):
        result, error_msg = self.employee2.doesNameExists()
        self.assertEqual(False, result)

    def test_doesNameExists_incorrect(self):

        self.employee2.user.username = self.username1
        result, error_msg = self.employee2.doesNameExists()
        self.assertEqual(True, result)

    def test_doesNameExists_correct_after_modify(self):
        self.employee2.user.username = "newName"
        result, error_msg = self.employee2.doesNameExists()
        self.assertEqual(False, result)

class UnitTestsDepartment(TestCase):
    dep1_name = "d1"
    department3 = None
    @classmethod
    def setUpTestData(cls):
        superuser = user = User.objects.create_superuser("super", "fakemail2@mail.com", "mdp")
        superuser.save()
        store = Store(name="store", user=superuser)
        store.save()
        department1 = Department(name=cls.dep1_name, store=store)
        department1.save()
        department2 = Department(name="d2", store=store)
        department2.save()
        cls.department3 = Department(name="d3", store=store)
        cls.department3.save()


    def test_doesNameExists_correct(self):
        result, error_msg = self.department3.doesNameExists()
        self.assertEqual(False, result)

    def test_doesNameExists_incorrect(self):
        self.department3.name = self.dep1_name
        result, error_msg = self.department3.doesNameExists()
        self.assertEqual(True, result)

    def test_doesNameExists_correct_after_Modify(self):
        self.department3.name = "new_name"
        result, error_msg = self.department3.doesNameExists()
        self.assertEqual(False, result)

class RayonViewTest(TestCase):
    username1 = "user1"
    password1 = "pass1"

    username2 = "user2"
    password2 = "pass2"

    super_username = "superuser"
    super_password = "superpass"

    @classmethod
    def setUpTestData(cls):
        superuser = user = User.objects.create_superuser(cls.super_username, "fakemail2@mail.com", cls.super_password)
        superuser.save()
        store = Store(name="store", user=superuser)
        store.save()
        department1 = Department(name="d1", store=store)
        department1.save()
        department2 = Department(name="d2", store=store)
        department2.save()
        user1 = User.objects.create_user(cls.username1, "fakemail@mail.com", cls.password1)
        user1.save()
        employee1 = Employee(user=user1, phonenumber="0505050505", department=department1)
        employee1.save()
        user2 = User.objects.create_user(cls.username2, "fakemail@mail.com", cls.password2)
        user2.save()
        employee2 = Employee(user=user2, phonenumber="0505050506", department=department2)
        employee2.save()

    def test_acces_rayon_non_identifie(self):
        reponse = self.client.get(reverse('rayon'))
        self.assertEqual(reponse.status_code, 302)  # la requête s'est bien déroulée
        self.assertRedirects(reponse, '/StoreManager/connexion?next=/StoreManager/rayon')

    def test_acces_rayon_identifie(self):
        self.client.login(username = self.username1, password = self.password1)
        reponse = self.client.get(reverse('rayon'))
        self.assertEqual(reponse.status_code, 200)  # la requête s'est bien déroulée
        self.assertContains(reponse, "Bienvenue, "+self.username1+" !")

    def test_ajoute_produit(self):
        self.client.login(username=self.username1, password=self.password1)
        num_product = len(Product.objects.all())
        reponse = self.client.post(reverse('rayon'),{'add': ['Ajouter une ligne']})
        self.assertEqual(reponse.status_code, 200)  # la requête s'est bien déroulée
        self.assertEqual(num_product+1, len(Product.objects.all()))


class ConnexionViewTests(TestCase):
    username = "fakeusername"
    password = "fakepassword"


    @classmethod
    def setUpTestData(cls):
        superuser = user = User.objects.create_superuser("boss", "fakemail2@mail.com", "bossmdp")
        superuser.save()
        store = Store(name="store", user=superuser)
        store.save()
        department = Department(name="d1", store=store)
        department.save()
        user = User.objects.create_user(cls.username, "fakemail@mail.com", cls.password)
        user.save()
        employee = Employee(user= user,phonenumber = "0505050505", department = department)
        employee.save()

    def test_connexion_echec(self):
        """ Teste le fait de rentrer de mauvais identifiants """
        data = {
            'username': 'baduser',
            'password': 'Badpass',
        }
        reponse = self.client.post(reverse('connexion'), data)
        self.assertEqual(reponse.status_code, 200) #la requête s'est bien détroulée
        self.assertContains(reponse, "Utilisateur inconnu ou mauvais de mot de passe.")

    def test_connexion_mauvais_mot_de_passe(self):
        """ Teste le fait de rentrer un mauvais mot de passe """
        data = {
            'username': self.username,
            'password': "badpassword",
        }
        reponse = self.client.post(reverse('connexion'), data)
        self.assertEqual(reponse.status_code, 200) #la requête s'est bien détroulée
        self.assertContains(reponse, "Utilisateur inconnu ou mauvais de mot de passe.")

    def test_connexion_mauvais_identifiant(self):
        """ Teste le fait de rentrer un mauvais identifiant """
        data = {
            'username': "badId",
            'password': self.password,
        }
        reponse = self.client.post(reverse('connexion'), data)
        self.assertEqual(reponse.status_code, 200)  # la requête s'est bien détroulée
        self.assertContains(reponse, "Utilisateur inconnu ou mauvais de mot de passe.")

    def test_connexion_reussie(self):
        """ Teste une connexion avec de bons identifiants """
        data = {
            'username': self.username,
            'password': self.password,
        }
        reponse = self.client.post(reverse('connexion'), data)

        self.assertEqual(reponse.status_code, 200)  # la requête s'est bien détroulée
        self.assertNotContains(reponse, "Utilisateur inconnu ou mauvais de mot de passe.")
        self.assertContains(reponse, "Vous êtes connecté,")

    def test_deconnexion(self):
        """ Teste une deconnexion"""
        reponse = self.client.get(reverse('deconnexion'))

        self.assertEqual(reponse.status_code, 302)  # la requête s'est bien déroulée
        self.assertRedirects(reponse, reverse('connexion'))
