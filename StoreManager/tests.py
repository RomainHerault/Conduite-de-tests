from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from StoreManager.models import Employee, Department, Store, Product


class EmployeeTests(TestCase):
    def test_truc_avec_employee(self):
        # ecrire un test avec les employees
        pass

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
        reponse = self.client.post(reverse('rayon'),{'add_product': ['Ajouter une ligne']})
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
