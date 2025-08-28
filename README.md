# Système de prise de réservation dans un restaurant

## Description

Ce projet est une API RESTful développée avec Django Rest Framework (DRF) pour gérer la prise de réservation de tables ou de salons dans un restaurant. L'API permet aux utilisateurs de créer, consulter, modifier et supprimer des réservations, tout en assurant une gestion efficace des données via une base de données PostgreSQL.

## Prérequis
Avant de commencer, assurez-vous d'avoir les outils suivants installés :

- Python 3.8+
- PostgreSQL
- pip (gestionnaire de paquets Python)
- Git

## Installation

Cloner le dépôtClonez le projet depuis GitHub :

```BASH
git clone https://github.com/Giovanni98-git/reservenow.git
cd reservenow
```

Créer un environnement virtuelCréez et activez un environnement virtuel pour isoler les dépendances :

```BASH
python -m venv env
source env/bin/activate # Sur Windows : env\Scripts\activate
```

## Installer les dépendances

Installez les packages requis listés dans requirements.txt :

```BASH
pip install -r requirements.txt
```

## Configurer la base de données

Assurez-vous que PostgreSQL est installé et en cours d'exécution.
Créez une base de données pour le projet :

```SQL
CREATE DATABASE votre_database;
```

## Configurer les variables d'environnement

Créez un fichier .env à la racine du projet et ajoutez les informations suivantes :

```BASH
DATABASE_NAME=votre_database
DATABASE_USER=votre_utilisateur
DATABASE_PASSWORD=votre_mot_de_passe
DATABASE_HOST=localhost
DATABASE_PORT=5432
SECRET_KEY=votre_cle_secrete_django
```

Remplacez votre_utilisateur, votre_mot_de_passe, et votre_cle_secrete_django par vos propres valeurs. Vous pouvez générer une clé secrète Django avec un générateur en ligne ou via un script Python.

## Appliquer les migrations

Configurez la base de données en exécutant les migrations Django :

```BASH
python manage.py makemigrations
python manage.py migrate
```

## Lancer le serveur

Démarrez le serveur de développement :

```BASH
python manage.py runserver
```

L'API sera accessible à l'adresse *http://localhost:8000*.

## Structure du projet

- **api/** : Contient les modèles, vues, sérialiseurs et URLs pour gérer les réservations.
- **settings.py** : Configuration Django, incluant la connexion à PostgreSQL.
- **.env** : Fichier pour stocker les variables d'environnement sensibles (non inclus dans le contrôle de version).
- **LICENSE** : Fichier contenant la licence MIT du projet.

## Utilisation de l'API et Documentation

Pour explorer tous les endpoints disponibles et leurs détails, accédez à l'interface Swagger à l'adresse *http://localhost:8000/ui/* une fois le serveur lancé.

## Contribution

- Forkez le dépôt.
- Créez une branche pour votre fonctionnalité (**git checkout -b feature/nouvelle-fonctionnalite**).
- Commitez vos modifications (**git commit -m "Ajout de nouvelle fonctionnalité"**).
- Poussez votre branche (**git push origin feature/nouvelle-fonctionnalite**).
- Créez une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
