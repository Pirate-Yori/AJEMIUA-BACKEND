from datetime import timezone

from django.db import models
from django.contrib.auth.models import User,AbstractUser

class CustomUser(AbstractUser):
    matricule = models.CharField(max_length=15,unique=True)
    telephone = models.CharField(max_length=15,unique=True)
    nom = models.CharField(max_length=15)
    prenom = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=11)

    roles = models.ManyToManyField('Role',related_name='utilisateurs')
    def __str__(self):
        return f"{self.matricule}--{','.join([r.type for r in self.roles.all()])}"

class Role(models.Model):
    type = models.CharField(max_length=20,unique=True)
    auteur_role = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.type}--{self.auteur_role}"

class UserRole(models.Model):
    user = models.ForeignKey('CustomUser',on_delete=models.CASCADE)
    role = models.ForeignKey('Role',on_delete=models.CASCADE)
    date_attribution = models.DateTimeField(auto_now_add=True)

     #Ici ca veut qu'on peut pas avoir deux mm enregistrementd

    def str(self):
            return f"{self.user.matricule}--{self.role.type}"

    class Meta:
        unique_together = ('user','role')



class Actualite(models.Model):
    titre = models.CharField(max_length=30)
    contenu = models.TextField()
    media= models.ImageField(upload_to='media/')
    date = models.DateField()
    type = models.CharField(max_length=20)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titre}--{self.date}"

class RappelIslamique(models.Model):
    titre = models.CharField(max_length=30)
    contenu = models.TextField()
    type = models.CharField(max_length=20)
    user = models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

class Evenement(models.Model):
    titre = models.CharField(max_length=30)
    description = models.TextField()
    date = models.DateField()
    media= models.ImageField(upload_to='media/')
    type = models.CharField(max_length=20)
    #fichier = models.FileField(upload_to='media/')
    user = models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titre}--{self.date}"

class RessourceIslamique(models.Model):
    titre = models.CharField(max_length=30)
    contenu = models.TextField()
    type = models.CharField(max_length=20)
    fichier= models.ImageField(upload_to='media/')
    user = models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.titre

class Archive(models.Model):
    titre = models.CharField(max_length=30)
    contenu = models.TextField()
    type = models.CharField(max_length=20)
    user = models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.titre




