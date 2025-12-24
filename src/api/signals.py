from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import UserRole
from accounts.models import CustomUser


@receiver(m2m_changed, sender=CustomUser.roles.through)
def sync_user_role_table(sender, instance, action, pk_set, **kwargs):
    """
    Synchronise la table UserRole quand on assigne/désassigne des rôles via ManyToMany
    """
    if action == 'post_add':
        # Quand des rôles sont ajoutés
        from api.models import Role
        for role_id in pk_set:
            role = Role.objects.get(pk=role_id)
            # Créer l'entrée UserRole si elle n'existe pas
            UserRole.objects.get_or_create(
                user=instance,
                role=role
            )
    
    elif action == 'post_remove':
        # Quand des rôles sont retirés
        from api.models import Role
        for role_id in pk_set:
            role = Role.objects.get(pk=role_id)
            # Supprimer l'entrée UserRole
            UserRole.objects.filter(
                user=instance,
                role=role
            ).delete()
    
    elif action == 'post_clear':
        # Quand tous les rôles sont retirés
        UserRole.objects.filter(user=instance).delete()

