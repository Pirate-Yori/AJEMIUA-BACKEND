from django.contrib import admin
from .models import  CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'telephone', 'get_roles')
    search_fields = ('matricule', 'nom', 'prenom')

    def get_roles(self, obj):
        return ", ".join([role.nom for role in obj.roles.all()])
    get_roles.short_description = "Rôles"

