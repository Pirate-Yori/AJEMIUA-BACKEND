from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, matricule, nom, prenom, telephone, password=None, **extra_fields):
        if not matricule:
            raise ValueError("Le matricule est obligatoire")

        user = self.model(
            matricule=matricule,
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricule, nom, prenom, telephone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(matricule, nom, prenom, telephone, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # on supprime le champ username


    matricule = models.CharField(max_length=15, unique=True, null=True, blank=True)
    telephone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    nom = models.CharField(max_length=15)
    prenom = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_member = models.BooleanField(default=True)  # Pour activer/désactiver un utilisateur (True = actif, False = désactivé)
    password_changed = models.BooleanField(default=False)  # Pour forcer le changement de mot de passe à la première connexion
    



    roles = models.ManyToManyField('api.Role', related_name='utilisateurs')

    USERNAME_FIELD = "matricule"
    REQUIRED_FIELDS = ["nom", "prenom", "telephone"]
    objects = CustomUserManager()


    def __str__(self):
        return f"{self.matricule} -- {','.join([r.type for r in self.roles.all()])}"
