from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def assign_default_role_to_new_user(sender, instance, created, **kwargs):
    """
    Assigner automatiquement le rôle "étudiant" à chaque nouvel utilisateur.
    """
    if created:
        from api.models import Role
        
        # Créer ou récupérer le rôle "étudiant" par défaut
        etudiant_role, _ = Role.objects.get_or_create(type="étudiant")
        
        # Assigner le rôle à l'utilisateur s'il ne l'a pas déjà
        if not instance.roles.filter(type="étudiant").exists():
            instance.roles.add(etudiant_role)


# Signal de notification supprimé - les utilisateurs sont maintenant créés uniquement par l'admin


@receiver(post_migrate)
def create_default_roles_and_admin(sender, **kwargs):
    """
    Crée automatiquement les rôles par défaut et un administrateur après les migrations.
    """
    # Vérifier que c'est bien l'app accounts qui a migré
    if sender.name == 'accounts':
        from api.models import Role

        # Créer les rôles par défaut s'ils n'existent pas
        etudiant_role, _ = Role.objects.get_or_create(type="étudiant")
        admin_role, _ = Role.objects.get_or_create(type="admin")
        
        print(f"✅ Rôles par défaut créés/vérifiés: 'étudiant', 'admin'")

        # Créer l'administrateur par défaut s'il n'existe pas
        if not CustomUser.objects.filter(matricule="ADMIN001").exists():
            try:
                admin = CustomUser.objects.create_user(
                    matricule="ADMIN001",
                    nom="Admin",
                    prenom="System",
                    telephone="0000000000",
                    password="adminpassword",
                )
                # Donner le rôle admin
                admin.roles.add(admin_role)
                admin.is_member = True  # Admin actif par défaut
                admin.password_changed = True  # L'admin peut garder son mot de passe par défaut
                admin.save()
                print("✅ Administrateur par défaut créé avec succès!")
                print("   Matricule: ADMIN001")
                print("   Mot de passe: adminpassword")
            except Exception as e:
                print(f"❌ Erreur lors de la création de l'administrateur par défaut: {e}")

