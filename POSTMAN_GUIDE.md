# Guide Postman - API AJEMIUA

**URL de base** : `http://127.0.0.1:8000`

---

## 🔐 1. CONNEXION ADMIN

**POST** `http://127.0.0.1:8000/auth/admin/login/`

**Body (JSON)** :
```json
{
    "matricule": "ADMIN001",
    "password": "adminpassword"
}
```

**Réponse** : Copier le `access` token pour les requêtes suivantes.

---

## 👥 2. GESTION UTILISATEURS (ADMIN)

### Liste tous les utilisateurs
**GET** `http://127.0.0.1:8000/auth/admin/users/`  
**Headers** : `Authorization: Bearer <ACCESS_TOKEN>`

### Détails d'un utilisateur
**GET** `http://127.0.0.1:8000/auth/admin/users/<id>/`  
**Headers** : `Authorization: Bearer <ACCESS_TOKEN>`

### Modifier un utilisateur
**PATCH** `http://127.0.0.1:8000/auth/admin/users/<id>/`  
**Headers** : `Authorization: Bearer <ACCESS_TOKEN>`

**Body (JSON)** :
```json
{
    "nom": "NouveauNom",
    "prenom": "NouveauPrenom",
    "telephone": "0987654321",
    "is_member": true,
    "roles": [2, 3]
}
```

**Pour désactiver** : `{"is_member": false}`  
**Pour activer** : `{"is_member": true}`

### Importer des utilisateurs depuis Excel
**POST** `http://127.0.0.1:8000/auth/admin/users/import-excel/`  
**Headers** : `Authorization: Bearer <ACCESS_TOKEN>`

**Body** : `form-data`
- `file` (File) : Sélectionner le fichier Excel
- `default_password` (Text, optionnel) : `Etudiant123`

**Format Excel requis** :
| matricule | nom | prenom | telephone |
|-----------|-----|--------|-----------|
| MAT001    | Doe | John   | 1234567890|

**Réponse** : Un fichier Excel sera téléchargé avec les utilisateurs créés et leurs mots de passe.

---

## 🔑 3. CONNEXION UTILISATEUR

**POST** `http://127.0.0.1:8000/login/`

**Body (JSON)** :
```json
{
    "matricule": "MAT001",
    "password": "Etudiant123"
}
```

**Réponse** : Si `password_change_required: true`, l'utilisateur doit changer son mot de passe.

---

## 🔄 4. CHANGEMENT DE MOT DE PASSE

**POST** `http://127.0.0.1:8000/change-password/`  
**Headers** : `Authorization: Bearer <ACCESS_TOKEN>`

**Body (JSON)** :
```json
{
    "old_password": "Etudiant123",
    "new_password": "MonNouveauMotDePasse123"
}
```

---

## 👤 5. MES INFORMATIONS

**GET** `http://127.0.0.1:8000/user/`  
**Headers** : `Authorization: Bearer <ACCESS_TOKEN>`

**PATCH** `http://127.0.0.1:8000/user/` (modifier)  
**Headers** : `Authorization: Bearer <ACCESS_TOKEN>`

**Body (JSON)** :
```json
{
    "nom": "NouveauNom",
    "prenom": "NouveauPrenom"
}
```

---

## 🔄 6. TOKENS

### Rafraîchir le token
**POST** `http://127.0.0.1:8000/token/refresh/`

**Body (JSON)** :
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Déconnexion
**POST** `http://127.0.0.1:8000/logout/`  
**Headers** : `Authorization: Bearer <ACCESS_TOKEN>`

**Body (JSON)** :
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 📋 SCÉNARIO DE TEST

1. **Connexion Admin** : `POST /auth/admin/login/` → Copier le token
2. **Importer Excel** : `POST /auth/admin/users/import-excel/` → Télécharger le fichier Excel
3. **Connexion utilisateur** : `POST /login/` avec matricule et mot de passe du fichier Excel
4. **Changer mot de passe** : `POST /change-password/` si `password_change_required: true`

---

## ⚠️ NOTES IMPORTANTES

- **Admin par défaut** : `ADMIN001` / `adminpassword` (créé automatiquement)
- **Rôle par défaut** : Tous les nouveaux utilisateurs reçoivent le rôle "étudiant"
- **Champs cachés** : `is_superuser`, `is_staff`, `is_active`, `is_admin`, `password` ne sont jamais retournés
- **Token** : Inclure `Authorization: Bearer <token>` pour toutes les routes admin

---

## 📞 ENDPOINTS

### Utilisateur
- `POST /login/` - Connexion
- `POST /change-password/` - Changer mot de passe
- `GET /user/` - Mes informations
- `PATCH /user/` - Modifier mes informations
- `POST /logout/` - Déconnexion
- `POST /token/refresh/` - Rafraîchir token

### Admin
- `POST /auth/admin/login/` - Connexion admin
- `GET /auth/admin/users/` - Liste utilisateurs
- `GET /auth/admin/users/<id>/` - Détails utilisateur
- `PATCH /auth/admin/users/<id>/` - Modifier utilisateur
- `POST /auth/admin/users/import-excel/` - Importer Excel
