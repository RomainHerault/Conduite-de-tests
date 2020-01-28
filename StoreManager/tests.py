from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from StoreManager.models import Employee, Department, Store


class EmployeeTests(TestCase):
    def test_truc_avec_employee(self):
        # ecrire un test avec les employees
        pass


class connexionTests(TestCase):
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

        self.assertEqual(reponse.status_code, 302)  # la requête s'est bien détroulée
        self.assertRedirects(reponse, reverse('connexion'))
