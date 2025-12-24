"""
Script pour créer un utilisateur administrateur
Usage: python create_admin.py
"""
import os
import sys
import django

# Configuration du chemin Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import CustomUser
from api.models import Role

def create_admin():
    print("=" * 50)
    print("Création d'un utilisateur administrateur")
    print("=" * 50)
    
    matricule = input("Matricule: ").strip()
    nom = input("Nom: ").strip()
    prenom = input("Prénom: ").strip()
    telephone = input("Téléphone: ").strip()
    password = input("Mot de passe: ").strip()
    
    # Vérifier si l'utilisateur existe déjà
    if CustomUser.objects.filter(matricule=matricule).exists():
        print(f"\n❌ Erreur: Un utilisateur avec le matricule '{matricule}' existe déjà.")
        return
    
    # Créer l'utilisateur admin avec rôle "admin" (sans superuser)
    try:
        admin_role, _ = Role.objects.get_or_create(type="admin")

        admin = CustomUser.objects.create_user(
            matricule=matricule,
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            password=password,
        )
        admin.roles.add(admin_role)
        # On s'assure qu'il peut se connecter via l'API
        admin.is_member = True
        admin.save()
        
        print("\n✅ Utilisateur administrateur créé avec succès!")
        print(f"   Matricule: {admin.matricule}")
        print(f"   Nom: {admin.nom} {admin.prenom}")
        print(f"   is_admin: {admin.is_admin}")
        print(f"   is_member: {admin.is_member}")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la création: {e}")

if __name__ == "__main__":
    create_admin()

