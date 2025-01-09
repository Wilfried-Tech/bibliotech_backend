# BiblioTech :books:

BiblioTech est une API pour la gestion d'une bibliothèque avec un pannel d'administration.

## :white_check_mark: Prérequis

### :gear: Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### :hammer_and_wrench: Configurer le super utilisateur

```bash
python manage.py migrate
python manage.py createsuperuser
```

#### Lancer le serveur

```bash
python manage.py runserver
```

## :sparkles: Fonctionnement

### :key: Authentification

Pour accéder à l'API, il faut s'authentifier avec un token JWT. Pour cela, il faut envoyer une requête POST à l'URL `/api/login/` avec les identifiants de l'utilisateur. et récupérer un access token et un refresh token.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}' http://localhost:8000/api/login/
```

### Gestion des Auteurs et des Catégories

Actuellement, uniquement les administrateurs peuvent ajouter des auteurs et des catégories. Pour cela, il faut envoyer une requête POST à l'URL `/api/authors/` ou `/api/categories/` ou encore par le pannel d'administration.

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"first_name": "J.K. Rowling"}' http://localhost:8000/api/authors/
```

### Gestion des Livres

De la même manière que pour les auteurs et les catégories, il est possible d'ajouter des livres. via une requête POST à l'URL `/api/books/` ou par le pannel d'administration. les utilisateurs peuvent consulter les livres sans authentification.

### Gestion des Emprunts

Les utilisateurs peuvent emprunter des livres en envoyant une requête POST à l'URL `/api/books/<book_id>/borrow/` avec un token d'authentification.
l'endpoint `/api/borrows/` permet de consulter les emprunts de l'utilisateur connecté. si l'utilisateur est un administrateur, il peut consulter les emprunts de tous les utilisateurs.

ont peut aussi rendre un livre en envoyant une requête POST à l'URL `/api/books/<book_id>/return/` avec un token d'authentification.

un utilisateur ne peut pas emprunter plus de 5 livres en même temps.
la durée de l'emprunt est defini à l'enregistrement de l'emprunt.

### Gestion des Utilisateurs

Les utilisateurs peuvent s'inscrire en envoyant une requête POST à l'URL `/api/register/` avec un nom d'utilisateur, un email et un mot de passe.

uniquement les administrateurs peuvent consulter les utilisateurs en envoyant une requête GET à l'URL `/api/users/`.

seul les utilisateurs peuvent changer leurs informations en envoyant une requête PATCH à l'URL `/api/users/<user_id>/` avec un token d'authentification.

les administrateurs peuvent bamir un utilisateur en envoyant une requête POST à l'URL `/api/users/<user_id>/ban/` ou le débannir en envoyant une requête DELETE sur la même URL.

Pour plus de détails, consulter la documentation de l'API. (en cours de développement)

## :rocket: Fonctionnalités

- [x] Gestion des livres
- [x] Gestion des auteurs
- [x] Gestion des emprunts
- [x] Gestion des utilisateurs
- [x] Gestion des catégories
- [x] Authentification par JWT
- [x] Pannel d'administration
- [x] Tests unitaires
- [x] Pagination
- [ ] Authentification par OAuth
- [ ] Documentation de l'API
- [ ] Filtrage et recherche
- [ ] Frontend avec Flutter

## :computer: Technologies utilisées

- Python
- Django
- Django Rest Framework

## :iphone: Frontend Flutter

[bibliotech](https://github.com/Wilfried-Tech/bibliotech)
