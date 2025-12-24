"""
Script pour synchroniser les données existantes dans la table UserRole
Usage: python sync_userroles.py
"""
import os
import sys
import django

# Configuration du chemin Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import CustomUser
from api.models import UserRole, Role

def sync_user_roles():
    print("=" * 60)
    print("Synchronisation des UserRole depuis CustomUser.roles")
    print("=" * 60)
    
    # Supprimer toutes les entrées existantes pour repartir à zéro
    UserRole.objects.all().delete()
    print("✅ Anciennes entrées UserRole supprimées")
    
    # Parcourir tous les utilisateurs
    users = CustomUser.objects.all()
    total_synced = 0
    
    for user in users:
        # Récupérer tous les rôles de l'utilisateur via ManyToMany
        roles = user.roles.all()
        
        for role in roles:
            # Créer l'entrée UserRole
            user_role, created = UserRole.objects.get_or_create(
                user=user,
                role=role
            )
            if created:
                total_synced += 1
                print(f"✅ {user.matricule} -> {role.type}")
    
    print(f"\n✅ Synchronisation terminée: {total_synced} relations créées")
    print(f"   Total UserRole dans la base: {UserRole.objects.count()}")

if __name__ == "__main__":
    sync_user_roles()

