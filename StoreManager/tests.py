from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class EmployeeTests(TestCase):
    def test_truc_avec_employee(self):
        # ecrire un test avec les employees
        pass


class ViewTests(TestCase):
    def test_connexion_echec(self):
        """ Teste le fait de rentrer de mauvais identifiants """
        data = {
            'username': 'fakeuser',
            'password': 'Badpass',
        }
        reponse = self.client.post(reverse('StoreManager.views.connexion'), data)
        self.assertEqual(reponse.status_code, 200)
        #self.assertRedirects(reponse, reverse('mini_url.views.liste'))

