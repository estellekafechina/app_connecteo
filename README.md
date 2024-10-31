# Connecteo

Connecteo est une application de réseau social basée sur Django, permettant aux utilisateurs de se connecter, partager des publications, suivre d'autres utilisateurs et interagir avec leurs contenus.

## Prérequis
- Python 3.9 ou version supérieure
- Django 5.1.1
- PostgreSQL (pour la production)
- Docker et Docker Compose

## Installation

1. Clonez le projet :
   ```bash
   git clone git@github.com:estellekafechina/app_connecteo.git
   cd votre_projet
   ```

2. Créez et activez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Créez un fichier `.env` pour y définir les variables d'environnement, y compris `DJANGO_SECRET_KEY`.

5. Appliquez les migrations de la base de données :
   ```bash
   python manage.py migrate
   ```

6. Créez un superutilisateur pour accéder à l'administration :
   ```bash
   python manage.py createsuperuser
   ```

7. Lancez le serveur de développement :
   ```bash
   python manage.py runserver
   ```

## Fonctionnalités

- **Inscription et Connexion** : Les utilisateurs peuvent s'inscrire, recevoir un e-mail de confirmation, et se connecter.
- **Profils Utilisateurs** : Les utilisateurs peuvent consulter des profils, modifier leur propre profil, et suivre/désuivre d'autres utilisateurs.
- **Posts** : Les utilisateurs peuvent créer des posts avec du texte et des images.
- **Fil d'Actualité** : Chaque utilisateur peut voir les posts des utilisateurs qu'ils suivent.
- **Messagerie** : Messagerie intégrée pour envoyer des messages entre utilisateurs.

## Structure des Fichiers
- **core/** : Contient l'application principale, incluant les vues, modèles, formulaires et templates.
- **templates/** : Contient les fichiers HTML pour l'interface utilisateur.
- **static/** : Contient les fichiers CSS, JS, et autres fichiers statiques.

## Installation locale du projet

1. Clonez le projet :
    ```bash
    git clone git@github.com:estellekafechina/app_connecteo.git
    cd votre_projet
    ```

2. Créez et activez un environnement virtuel :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows : venv\Scripts\activate
    ```

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

4. Créez un fichier `.env` pour y définir les variables d'environnement, y compris `DJANGO_SECRET_KEY`.

5. Appliquez les migrations de la base de données :
    ```bash
    python manage.py migrate
    ```

6. Créez un superutilisateur pour accéder à l'administration :
    ```bash
    python manage.py createsuperuser
    ```

7. Lancez le serveur de développement :
    ```bash
    python manage.py runserver
    ```

## Déploiement avec Docker

### Préparation pour la Production

1. **Créez un fichier Dockerfile** à la racine du projet :
   ```dockerfile
   # Utiliser une image officielle Python

   # Définir le répertoire de travail
   

   # Installer les dépendances
 

   # Appliquer les migrations et collecter les fichiers statiques
   

   # Exposer le port sur lequel l'application tourne
   EXPOSE 8000

   # Lancer Gunicorn
   CMD ["gunicorn", "connecteo.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```

2. **Créez un fichier docker-compose.yml** à la racine du projet :
   ```yaml
   version: '3'

   services:
     web:
       build: .
       command: gunicorn connecteo.wsgi:application --bind 0.0.0.0:8000
       volumes:
         - .:/app
       ports:
         - "8000:8000"
       env_file:
         - .env
       depends_on:
         - db

     db:
       image: postgres
       environment:
         POSTGRES_DB: connecteo
         POSTGRES_USER: connecteo_user
         POSTGRES_PASSWORD: your_password
       volumes:
         - postgres_data:/var/lib/postgresql/data/

   volumes:
     postgres_data:
   ```

3. **Lancer l'application** avec Docker Compose :
   ```bash
   docker-compose up --build
   ```

### Gunicorn et Nginx (Production)
1. **Gunicorn** :
   - Gunicorn est déjà configuré dans le Dockerfile pour servir l'application.

2. **Nginx** :
   - Configurez Nginx comme reverse proxy pour Gunicorn afin de gérer les requêtes HTTP et les certificats SSL.
   - Créez un fichier de configuration pour Nginx :
     ```
     server {
         listen 80;
         server_name example.com www.example.com;

         location /static/ {
             alias /app/static/;
         }

         location / {
             proxy_pass http://web:8000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header X-Forwarded-Proto $scheme;
         }
     }
     ```

3. **Certificat SSL** : Utilisez Let's Encrypt pour sécuriser les communications avec un certificat SSL.

### Déploiement Cloud
- Déployez l'application sur un serveur comme **AWS EC2**, **DigitalOcean**, ou **Heroku**.
- Configurez un serveur de base de données en production, par exemple avec PostgreSQL.

### CI/CD
- **GitHub Actions** :
  - Utilisez un workflow GitHub Actions pour tester et déployer automatiquement l'application sur le serveur.
  - Créez un fichier `.github/workflows/deploy.yml` pour automatiser le déploiement après chaque push sur la branche principale.

- **Script de déploiement** : Utilisez un script `deploy.sh` sur le serveur pour mettre à jour le code, appliquer les migrations, collecter les fichiers statiques, et redémarrer Gunicorn.

## Utilisation
- Lancez l'application avec Docker :
  ```bash
  docker-compose up -d
  ```
- Pour accéder à l'application, ouvrez votre navigateur et entrez votre domaine configuré.

## Technologies Utilisées
- **Backend** : Django
- **Frontend** : HTML, CSS, JavaScript (Bootstrap, FontAwesome)
- **Serveur d'Application** : Gunicorn
- **Reverse Proxy** : Nginx
- **Base de Données** : SQLite (développement), PostgreSQL (production)
- **Conteneurisation** : Docker, Docker Compose

## Contribution
Les contributions sont les bienvenues ! Veuillez créer une branche, apporter vos modifications et soumettre une pull request.

1. Clonez le repo et créez une nouvelle branche :
   ```bash
   git checkout -b feature/nom_de_la_fonctionnalité
   ```
2. Apportez vos modifications et committez-les :
   ```bash
   git commit -m "Ajout de la fonctionnalité X"
   ```
3. Poussez vers la branche :
   ```bash
   git push origin feature/nom_de_la_fonctionnalité
   ```
4. Ouvrez une pull request sur GitHub.

## Licence
Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

