from django.urls import path
from rest_framework import routers

from .views import  RoleViewSet, ActualiteViewSet, EvenementViewSet,ArchiveViewSet,RappelIslamiqueViewSet,RessourceIslamiqueViewSet,UserRoleViewSet

router = routers.DefaultRouter()


#route pour les roles here
router.register('roles',RoleViewSet)
router.register('actualites',ActualiteViewSet)
router.register('evenements',EvenementViewSet)
router.register('archives',ArchiveViewSet)
router.register('rappel-islamique',RappelIslamiqueViewSet)
router.register('ressourceislamique',RessourceIslamiqueViewSet)
router.register('userroles',UserRoleViewSet)
