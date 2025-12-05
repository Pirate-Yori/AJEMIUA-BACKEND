# users/views.py

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdminUserCustom
from .serializers import AdminLoginSerializer

from . import serializers
from .models import CustomUser

User = get_user_model()

class UserRegisterationAPIView(GenericAPIView):
    """
    An endpoint for the client to create a new User.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegisterationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "Votre inscription a été reçue. Un administrateur doit valider votre compte."},
            status=status.HTTP_201_CREATED
        )

class UserLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        # Vérifier si validé par l’admin
        if not user.is_member:
            return Response(
                {"detail": "Votre compte n’a pas encore été validé par l’administrateur."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Génération des tokens
        token = RefreshToken.for_user(user)

        data = serializers.CustomUserSerializer(user).data
        data["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token),
        }

        return Response(data, status=status.HTTP_200_OK)


class UserLogoutAPIView(GenericAPIView):
    """
    An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user information
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user



class AdminLoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = AdminLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token = RefreshToken.for_user(user)

        return Response({
            "admin": serializers.CustomUserSerializer(user).data,
            "tokens": {
                "refresh": str(token),
                "access": str(token.access_token)
            }
        })



class AdminUserListAPIView(ListAPIView):
    """
    Liste tous les utilisateurs (pour l'admin)
    Peut filtrer par is_member avec le paramètre ?is_member=true/false
    """
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    serializer_class = serializers.AdminUserSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        is_member = self.request.query_params.get('is_member', None)
        
        if is_member is not None:
            is_member_bool = is_member.lower() == 'true'
            queryset = queryset.filter(is_member=is_member_bool)
        
        return queryset.order_by('-date_joined')


class PendingUsersAPIView(ListAPIView):
    """
    Liste tous les utilisateurs en attente d'approbation (is_member=False)
    """
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    serializer_class = serializers.AdminUserSerializer
    
    def get_queryset(self):
        return User.objects.filter(is_member=False).order_by('-date_joined')


class ApprovedUsersAPIView(ListAPIView):
    """
    Liste tous les utilisateurs approuvés (is_member=True)
    """
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    serializer_class = serializers.AdminUserSerializer
    
    def get_queryset(self):
        return User.objects.filter(is_member=True).order_by('-date_joined')


class UserDetailAPIView(RetrieveUpdateAPIView):
    """
    Voir et modifier les détails d'un utilisateur spécifique (pour l'admin)
    """
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    serializer_class = serializers.AdminUserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'


class ApproveUserAPIView(APIView):
    """
    Approuve un utilisateur en mettant is_member à True
    """
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def patch(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "Utilisateur introuvable"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        if user.is_member:
            return Response(
                {"detail": "Cet utilisateur est déjà approuvé."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_member = True
        user.save()

        return Response(
            {
                "message": "Utilisateur approuvé avec succès.",
                "user": serializers.AdminUserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )


class DisapproveUserAPIView(APIView):
    """
    Désapprouve un utilisateur en mettant is_member à False
    """
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def patch(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "Utilisateur introuvable"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        if not user.is_member:
            return Response(
                {"detail": "Cet utilisateur n'est pas encore approuvé."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_member = False
        user.save()

        return Response(
            {
                "message": "Utilisateur désapprouvé avec succès.",
                "user": serializers.AdminUserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )

