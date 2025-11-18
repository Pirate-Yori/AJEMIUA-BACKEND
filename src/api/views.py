from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Role,UserRole,Actualite,Evenement,Archive,RessourceIslamique,RappelIslamique
from .serializers import  RoleSerializer, ActualiteSerializer, EvenementSerializer, \
    UserRoleSerializer, ArchiveSerializer, RappelIslamiqueSerializer, RessourceIslamiqueSerializer


# Create your views here.

#register



class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class ActualiteViewSet(viewsets.ModelViewSet):
    queryset = Actualite.objects.all()
    serializer_class = ActualiteSerializer

class EvenementViewSet(viewsets.ModelViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    permission_classes = [IsAuthenticated]

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

