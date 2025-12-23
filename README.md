## README pour le Dépôt Backend (Django REST API)

### Plateforme SaaS de Gestion Commerciale - Backend

Ce dépôt contient le code de l'API REST du projet, propulsé par **Django** et **Django REST Framework (DRF)**. Il gère toute la logique métier, la base de données, l'authentification et les échanges de données avec les applications Web et Mobile.

-----

### Technologies Clés

  * **Framework:** Django 5 + Django REST Framework (DRF) 
  * **Langage:** Python
  * **Base de Données:** PostgreSQL 
  * **Authentification:** JWT (SimpleJWT) 
  * **Tâches Asynchrones:** Celery + Redis 
  * **Conteneurisation:** Docker Compose 
  * **Tests:** Pytest 

-----

### Structure des Modules (Django Apps)

L'API est organisée en modules clairs pour une meilleure maintenabilité :

  * `authentication/`: Gestion de l'inscription, connexion (JWT), réinitialisation de mot de passe. 
  * `merchants/`: Gestion des informations du commerce (nom, logo, devise). 
  * `sellers/`: Création et gestion des profils vendeurs par les commerçants. 
  * `products/`: CRUD (Création, Lecture, Mise à jour, Suppression) des produits, stock et notifications. 
  * `sales/`: Enregistrement et historique des ventes, génération de tickets (PDF). 
  * `analytics/`: Calcul et exposition des indicateurs pour le tableau de bord (ventes, top produits, meilleur vendeur). 
  * `subscriptions/`: Gestion des plans Freemium (gratuit/payant) et quotas. 

-----

###  Démarrage Local (via Docker Compose)

1.  **Prérequis:** Assurez-vous d'avoir Docker et Docker Compose installés.
2.  **Configuration:** Créez un fichier `.env` à la racine du projet pour les variables d'environnement (clés secrètes, configuration PostgreSQL, etc.).
3.  **Lancement:**
    ```bash
    docker-compose up --build
    ```
4.  **Migrations:** Exécutez les migrations une fois les conteneurs démarrés :
    ```bash
    docker-compose exec web python manage.py migrate
    ```
5.  **Accès API:** L'API sera accessible sur `http://localhost:8000/api/v1/`. 
6.  **Documentation API:** La documentation interactive est disponible via **Swagger/drf-spectacular** sur `/api/schema/swagger/`. 

-----

