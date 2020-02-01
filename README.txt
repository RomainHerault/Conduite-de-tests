Conduite de test
Ce projet consiste en la gestion de magasin.

Prérequis
-Python3
-pip3
-pip3 install django

Installation
-Se déplacer à la racine du projet "Conduite-de-tests"
-Dans un shell exécuter la commande "python3 manage.py makemigrations"
-Dans un shell exécuter la commande "python3 manage.py migrate"
-Se déplacer dans le dossier "setup"
-Dans un shell exécuté la commande "python3 populate_database.py"
-Se déplacer à la racine du projet "Conduite-de-tests"
-Dans un shell exécuter la commande "python3 manage.py runserver"

Utilisations
Se connecter : http://127.0.0.1:8000/StoreManager/connexion
Produit : http://127.0.0.1:8000/StoreManager/produit
Rayon management : http://127.0.0.1:8000/StoreManager/rayon
Employe : http://127.0.0.1:8000/StoreManager/employe

Utilisateurs:
Chef de magasin : username=admin , password=admin
Chef de rayon : username=Michel , password=password
Chef de rayon : username=Jean , password=password
Chef de rayon : username=Alberto , password=password

Versioning
https://github.com/RomainHerault/Conduite-de-tests

Authors
Ponceau Nathanael
Herault Romain


