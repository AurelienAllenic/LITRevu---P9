# LITRevu
LITRevu est une application web développée avec Django qui permet aux utilisateurs de poster des critiques ou des demandes de critiques (tickets ou reviews) sur des œuvres littéraires. Les utilisateurs peuvent également suivre d'autres utilisateurs pour rester à jour avec leurs critiques et leurs activités.

# Fonctionnalités
Publication de critiques : Les utilisateurs peuvent publier leurs critiques sur des livres, des articles, des poèmes, etc.
Demandes de critiques : Les utilisateurs peuvent soumettre des demandes de critiques pour obtenir des retours sur leurs propres écrits.
Suivi d'utilisateurs : Les utilisateurs peuvent suivre d'autres utilisateurs pour voir leurs critiques et leurs activités.
Authentification utilisateur : L'application comprend un système d'authentification permettant aux utilisateurs de créer des comptes, de se connecter et de gérer leurs profils.

# Installation
Cloner le dépôt :
```
git clone https://github.com/AurelienAllenic/LITRevu---P9
```
Accéder au répertoire du projet :
```
cd ./LITRevu
```
Créer un environnement virtuel :
```
python -m venv env
```

Activer l'environnement virtuel :

Sur Windows :
```
.\env\Scripts\activate
```
Sur Linux/macOS :
```
source env/bin/activate
```
Installer les dépendances :
```
pip install -r requirements.txt
```
Effectuer les migrations de la base de données :
```
python manage.py migrate
```
Lancer le serveur de développement :
```
python manage.py runserver
```

# Utilisation
Une fois le serveur lancé, accédez à l'application dans votre navigateur à l'adresse http://localhost:8000/.

# Contribution
Les contributions sont les bienvenues ! Pour contribuer à ce projet, veuillez suivre les étapes suivantes :

# Forker le projet
Créer une branche pour votre fonctionnalité (git checkout -b feature/NomDeLaFonctionnalite)
Commiter vos modifications (git commit -am 'Ajouter une nouvelle fonctionnalité')
Pusher la branche sur votre fork (git push origin feature/NomDeLaFonctionnalite)
Créer un Pull Request
Auteurs
Votre Nom (@votre-utilisateur)

# Licence
Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus d'informations.