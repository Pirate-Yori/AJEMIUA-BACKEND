# Guide de Test Postman - API AJEMIUA

## Configuration de base
- **URL de base** : `http://127.0.0.1:8000` ou `http://localhost:8000`
- **Headers par défaut** : `Content-Type: application/json`

---

## 📝 ÉTAPE 1 : INSCRIPTION D'UN UTILISATEUR

### 1.1 Inscription d'un nouvel utilisateur
**Méthode** : `POST`  
**URL** : `http://127.0.0.1:8000/register/`  
**Headers** :
```
Content-Type: application/json
```
**Body (raw JSON)** :
```json
{
    "matricule": "MAT001",
    "nom": "Doe",
    "prenom": "John",
    "telephone": "1234567890",
    "password": "password123"
}
```

**Réponse attendue** (201 Created) :
```json
{
    "message": "Votre inscription a été reçue. Un administrateur doit valider votre compte."
}
```

---

## 🔐 ÉTAPE 2 : CONNEXION ADMIN

### 2.1 Connexion Admin
**Méthode** : `POST`  
**URL** : `http://127.0.0.1:8000/auth/admin/login/`  
**Headers** :
```
Content-Type: application/json
```
**Body (raw JSON)** :
```json
{
    "matricule": "ADMIN001",
    "password": "adminpassword"
}
```

**Réponse attendue** (200 OK) :
```json
{
    "admin": {
        "id": 1,
        "matricule": "ADMIN001",
        "nom": "Admin",
        "prenom": "User",
        "telephone": "0987654321",
        "email": null,
        "date_joined": "2024-01-01T00:00:00Z",
        "is_member": true,
        "is_admin": true,
        "is_active": true,
        "is_staff": true,
        "roles": []
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

**⚠️ IMPORTANT** : Copiez le `access` token pour les requêtes suivantes !

---

## 👥 ÉTAPE 3 : GESTION DES UTILISATEURS (ADMIN)

### 3.1 Liste tous les utilisateurs
**Méthode** : `GET`  
**URL** : `http://127.0.0.1:8000/auth/admin/users/`  
**Headers** :
```
Content-Type: application/json
Authorization: Bearer <ACCESS_TOKEN>
```

**Réponse attendue** (200 OK) :
```json
[
    {
        "id": 2,
        "matricule": "MAT001",
        "nom": "Doe",
        "prenom": "John",
        "telephone": "1234567890",
        "email": null,
        "date_joined": "2024-01-01T00:00:00Z",
        "is_member": false,
        "is_admin": false,
        "is_active": true,
        "is_staff": false,
        "roles": []
    }
]
```

**Filtres optionnels** :
- `?is_member=true` : Liste uniquement les utilisateurs approuvés
- `?is_member=false` : Liste uniquement les utilisateurs en attente

**Exemple** : `http://127.0.0.1:8000/auth/admin/users/?is_member=false`

---

### 3.2 Liste des utilisateurs en attente
**Méthode** : `GET`  
**URL** : `http://127.0.0.1:8000/auth/admin/users/pending/`  
**Headers** :
```
Content-Type: application/json
Authorization: Bearer <ACCESS_TOKEN>
```

**Réponse attendue** (200 OK) : Liste des utilisateurs avec `is_member=false`

---

### 3.3 Liste des utilisateurs approuvés
**Méthode** : `GET`  
**URL** : `http://127.0.0.1:8000/auth/admin/users/approved/`  
**Headers** :
```
Content-Type: application/json
Authorization: Bearer <ACCESS_TOKEN>
```

**Réponse attendue** (200 OK) : Liste des utilisateurs avec `is_member=true`

---

### 3.4 Détails d'un utilisateur spécifique
**Méthode** : `GET`  
**URL** : `http://127.0.0.1:8000/auth/admin/users/<user_id>/`  
**Exemple** : `http://127.0.0.1:8000/auth/admin/users/2/`  
**Headers** :
```
Content-Type: application/json
Authorization: Bearer <ACCESS_TOKEN>
```

**Réponse attendue** (200 OK) :
```json
{
    "id": 2,
    "matricule": "MAT001",
    "nom": "Doe",
    "prenom": "John",
    "telephone": "1234567890",
    "email": null,
    "date_joined": "2024-01-01T00:00:00Z",
    "is_member": false,
    "is_admin": false,
    "is_active": true,
    "is_staff": false,
    "roles": []
}
```

---

### 3.5 Approuver un utilisateur
**Méthode** : `PATCH`  
**URL** : `http://127.0.0.1:8000/auth/admin/users/<user_id>/approve/`  
**Exemple** : `http://127.0.0.1:8000/auth/admin/users/2/approve/`  
**Headers** :
```
Content-Type: application/json
Authorization: Bearer <ACCESS_TOKEN>
```

**Body** : Aucun body nécessaire (ou body vide `{}`)

**Réponse attendue** (200 OK) :
```json
{
    "message": "Utilisateur approuvé avec succès.",
    "user": {
        "id": 2,
        "matricule": "MAT001",
        "nom": "Doe",
        "prenom": "John",
        "telephone": "1234567890",
        "email": null,
        "date_joined": "2024-01-01T00:00:00Z",
        "is_member": true,
        "is_admin": false,
        "is_active": true,
        "is_staff": false,
        "roles": []
    }
}
```

---

### 3.6 Désapprouver un utilisateur
**Méthode** : `PATCH`  
**URL** : `http://127.0.0.1:8000/auth/admin/users/<user_id>/disapprove/`  
**Exemple** : `http://127.0.0.1:8000/auth/admin/users/2/disapprove/`  
**Headers** :
```
Content-Type: application/json
Authorization: Bearer <ACCESS_TOKEN>
```

**Body** : Aucun body nécessaire (ou body vide `{}`)

**Réponse attendue** (200 OK) :
```json
{
    "message": "Utilisateur désapprouvé avec succès.",
    "user": {
        "id": 2,
        "matricule": "MAT001",
        "nom": "Doe",
        "prenom": "John",
        "telephone": "1234567890",
        "email": null,
        "date_joined": "2024-01-01T00:00:00Z",
        "is_member": false,
        "is_admin": false,
        "is_active": true,
        "is_staff": false,
        "roles": []
    }
}
```

---

## 🔑 ÉTAPE 4 : CONNEXION UTILISATEUR

### 4.1 Tentative de connexion (utilisateur non approuvé)
**Méthode** : `POST`  
**URL** : `http://127.0.0.1:8000/login/`  
**Headers** :
```
Content-Type: application/json
```
**Body (raw JSON)** :
```json
{
    "matricule": "MAT001",
    "password": "password123"
}
```

**Réponse attendue** (403 Forbidden) :
```json
{
    "detail": "Votre compte n'a pas encore été validé par l'administrateur."
}
```

---

### 4.2 Connexion (utilisateur approuvé)
**Méthode** : `POST`  
**URL** : `http://127.0.0.1:8000/login/`  
**Headers** :
```
Content-Type: application/json
```
**Body (raw JSON)** :
```json
{
    "matricule": "MAT001",
    "password": "password123"
}
```

**Réponse attendue** (200 OK) :
```json
{
    "id": 2,
    "matricule": "MAT001",
    "nom": "Doe",
    "prenom": "John",
    "telephone": "1234567890",
    "email": null,
    "date_joined": "2024-01-01T00:00:00Z",
    "is_member": true,
    "is_admin": false,
    "is_active": true,
    "is_staff": false,
    "roles": [],
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

---

## 🔄 ÉTAPE 5 : GESTION DES TOKENS

### 5.1 Rafraîchir le token
**Méthode** : `POST`  
**URL** : `http://127.0.0.1:8000/token/refresh/`  
**Headers** :
```
Content-Type: application/json
```
**Body (raw JSON)** :
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Réponse attendue** (200 OK) :
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 5.2 Déconnexion
**Méthode** : `POST`  
**URL** : `http://127.0.0.1:8000/logout/`  
**Headers** :
```
Content-Type: application/json
Authorization: Bearer <ACCESS_TOKEN>
```
**Body (raw JSON)** :
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Réponse attendue** (205 Reset Content) : Pas de contenu

---

## 👤 ÉTAPE 6 : INFORMATIONS UTILISATEUR

### 6.1 Obtenir ses propres informations
**Méthode** : `GET`  
**URL** : `http://127.0.0.1:8000/user/`  
**Headers** :
```
Content-Type: application/json
Authorization: Bearer <ACCESS_TOKEN>
```

**Réponse attendue** (200 OK) : Informations de l'utilisateur connecté

---

### 6.2 Modifier ses propres informations
**Méthode** : `PATCH` ou `PUT`  
**URL** : `http://127.0.0.1:8000/user/`  
**Headers** :
```
Content-Type: application/json
Authorization: Bearer <ACCESS_TOKEN>
```
**Body (raw JSON)** :
```json
{
    "nom": "NouveauNom",
    "prenom": "NouveauPrenom"
}
```

---

## 📋 SCÉNARIO DE TEST COMPLET

### Scénario 1 : Inscription et approbation complète

1. **Inscription** : `POST /register/` avec un nouvel utilisateur
2. **Connexion Admin** : `POST /auth/admin/login/` (copier le token)
3. **Voir les utilisateurs en attente** : `GET /auth/admin/users/pending/`
4. **Approuver l'utilisateur** : `PATCH /auth/admin/users/<id>/approve/`
5. **Connexion utilisateur** : `POST /login/` (devrait maintenant fonctionner)

### Scénario 2 : Test de sécurité

1. **Tentative de connexion non approuvée** : `POST /login/` (devrait échouer avec 403)
2. **Tentative d'accès admin sans token** : `GET /auth/admin/users/` (devrait échouer avec 401)
3. **Tentative d'accès admin avec token utilisateur** : `GET /auth/admin/users/` (devrait échouer avec 403)

---

## ⚠️ NOTES IMPORTANTES

1. **Créer un utilisateur admin** : Vous devez d'abord créer un utilisateur avec `is_admin=True` via Django shell ou Django admin
   ```python
   python manage.py shell
   from accounts.models import CustomUser
   admin = CustomUser.objects.create_user(
       matricule="ADMIN001",
       nom="Admin",
       prenom="User",
       telephone="0987654321",
       password="adminpassword"
   )
   admin.is_admin = True
   admin.is_member = True
   admin.save()
   ```

2. **Token d'authentification** : Pour toutes les routes admin, vous devez inclure le header :
   ```
   Authorization: Bearer <votre_access_token>
   ```

3. **Format des dates** : Les dates sont au format ISO 8601 (ex: `2024-01-01T00:00:00Z`)

4. **Codes de statut HTTP** :
   - `200` : Succès
   - `201` : Créé avec succès
   - `205` : Succès sans contenu (logout)
   - `400` : Requête invalide
   - `401` : Non authentifié
   - `403` : Non autorisé
   - `404` : Non trouvé

---

## 🚀 DÉMARRAGE DU SERVEUR

Avant de tester, assurez-vous que le serveur Django est démarré :

```bash
cd src
python manage.py runserver
```

Le serveur sera accessible sur `http://127.0.0.1:8000`

