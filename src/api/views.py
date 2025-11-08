from django.shortcuts import render
from rest_framework import viewsets

from .models import CustomUser,Role,UserRole,Actualite,Evenement,Archive,RessourceIslamique,RappelIslamique
from .serializers import CustomUserSerializer, RoleSerializer, ActualiteSerializer, EvenementSerializer, \
    UserRoleSerializer, ArchiveSerializer, RappelIslamiqueSerializer, RessourceIslamiqueSerializer


# Create your views here.

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class ActualiteViewSet(viewsets.ModelViewSet):
    queryset = Actualite.objects.all()
    serializer_class = ActualiteSerializer

class EvenementViewSet(viewsets.ModelViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

class RappelIslamiqueViewSet(viewsets.ModelViewSet):
    queryset = RappelIslamique.objects.all()
    serializer_class = RappelIslamiqueSerializer

class RessourceIslamiqueViewSet(viewsets.ModelViewSet):
    queryset = RessourceIslamique.objects.all()
    serializer_class = RessourceIslamiqueSerializer

