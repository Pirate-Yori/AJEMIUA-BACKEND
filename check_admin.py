"""
Script pour vérifier ou créer l'admin rapidement
Usage: python check_admin.py
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

def check_or_create_admin():
    print("=" * 60)
    print("Vérification/Création de l'administrateur")
    print("=" * 60)
    
    # Vérifier si l'admin existe
    admin = CustomUser.objects.filter(matricule="ADMIN001").first()
    
    if admin:
        print(f"\n✅ Admin trouvé:")
        print(f"   Matricule: {admin.matricule}")
        print(f"   Nom: {admin.nom} {admin.prenom}")
        print(f"   is_member: {admin.is_member}")
        print(f"   password_changed: {admin.password_changed}")
        
        # Vérifier le rôle admin
        admin_role = Role.objects.filter(type="admin").first()
        if admin_role:
            has_admin_role = admin.roles.filter(type="admin").exists()
            print(f"   Rôle admin: {'✅ Oui' if has_admin_role else '❌ Non'}")
            
            if not has_admin_role:
                admin.roles.add(admin_role)
                print("   ✅ Rôle admin ajouté!")
        else:
            print("   ⚠️ Le rôle 'admin' n'existe pas encore")
            admin_role, _ = Role.objects.get_or_create(type="admin")
            admin.roles.add(admin_role)
            print("   ✅ Rôle admin créé et ajouté!")
        
        # S'assurer que is_member est True
        if not admin.is_member:
            admin.is_member = True
            admin.save()
            print("   ✅ is_member mis à True!")
        
        print(f"\n🔑 Identifiants de connexion:")
        print(f"   Matricule: ADMIN001")
        print(f"   Mot de passe: adminpassword")
        
    else:
        print("\n❌ Admin non trouvé. Création en cours...")
        
        # Créer le rôle admin s'il n'existe pas
        admin_role, _ = Role.objects.get_or_create(type="admin")
        
        try:
            admin = CustomUser.objects.create_user(
                matricule="ADMIN001",
                nom="Admin",
                prenom="System",
                telephone="0000000000",
                password="adminpassword"
            )
            admin.roles.add(admin_role)
            admin.is_member = True
            admin.password_changed = True
            admin.save()
            
            print("✅ Administrateur créé avec succès!")
            print(f"\n🔑 Identifiants de connexion:")
            print(f"   Matricule: ADMIN001")
            print(f"   Mot de passe: adminpassword")
            
        except Exception as e:
            print(f"❌ Erreur lors de la création: {e}")

if __name__ == "__main__":
    check_or_create_admin()

