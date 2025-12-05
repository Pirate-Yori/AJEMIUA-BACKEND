from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def notify_admin_on_new_user(sender, instance, created, **kwargs):
    """
    Envoie une notification aux administrateurs lorsqu'un nouvel utilisateur s'inscrit.
    """
    if created and not instance.is_member:
        # Récupérer tous les administrateurs
        admins = CustomUser.objects.filter(is_admin=True, is_active=True)
        
        if admins.exists():
            # Préparer le message
            subject = f"Nouvelle demande d'inscription - {instance.matricule}"
            message = f"""
Bonjour,

Un nouvel utilisateur a fait une demande d'inscription :

- Matricule: {instance.matricule}
- Nom: {instance.nom}
- Prénom: {instance.prenom}
- Téléphone: {instance.telephone}
- Date d'inscription: {instance.date_joined.strftime('%d/%m/%Y à %H:%M')}

Veuillez approuver cet utilisateur en mettant is_member à True pour qu'il puisse se connecter.

Cordialement,
Système de gestion
            """
            
            # Récupérer les emails des admins
            admin_emails = [admin.email for admin in admins if admin.email]
            
            # Si aucun email n'est configuré, on peut logger ou utiliser une autre méthode
            if admin_emails:
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
                        recipient_list=admin_emails,
                        fail_silently=False,
                    )
                except Exception as e:
                    # Si l'envoi d'email échoue, on peut logger l'erreur
                    print(f"Erreur lors de l'envoi de l'email aux admins: {e}")
            else:
                # Si les admins n'ont pas d'email, on peut logger l'information
                print(f"NOUVELLE INSCRIPTION - Matricule: {instance.matricule}, Nom: {instance.nom} {instance.prenom}")
                print(f"Les administrateurs n'ont pas d'adresse email configurée.")


@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    """
    Crée automatiquement un administrateur par défaut après les migrations.
    """
    # Vérifier que c'est bien l'app accounts qui a migré
    if sender.name == 'accounts':
        if not CustomUser.objects.filter(matricule="ADMIN001").exists():
            try:
                admin = CustomUser.objects.create_superuser(
                    matricule="ADMIN001",
                    nom="Admin",
                    prenom="System",
                    telephone="0000000000",
                    password="adminpassword"
                )
                # S'assurer que l'admin est aussi membre pour pouvoir se connecter
                admin.is_member = True
                admin.save()
                print("✅ Administrateur par défaut créé avec succès!")
                print("   Matricule: ADMIN001")
                print("   Mot de passe: adminpassword")
            except Exception as e:
                print(f"❌ Erreur lors de la création de l'administrateur par défaut: {e}")

