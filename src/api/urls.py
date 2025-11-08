from rest_framework import routers

from .views import CustomUserViewSet, RoleViewSet, ActualiteViewSet, EvenementViewSet,ArchiveViewSet,RappelIslamiqueViewSet,RessourceIslamiqueViewSet,UserRoleViewSet

router = routers.DefaultRouter()
router.register('users',CustomUserViewSet)

#route pour les roles here
router.register('roles',RoleViewSet)
router.register('actualites',ActualiteViewSet)
router.register('evenements',EvenementViewSet)
router.register('archives',ArchiveViewSet)
router.register('rappel-islamique',RappelIslamiqueViewSet)
router.register('ressourceislamique',RessourceIslamiqueViewSet)
router.register('userroles',UserRoleViewSet)