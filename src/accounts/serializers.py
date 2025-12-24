# users/serializers.py

from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer pour les utilisateurs (exclut le mot de passe)
    """
    date_joined = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "matricule",
            "nom",
            "prenom",
            "telephone",
            "date_joined",
            "is_member",
            "password_changed",
            "roles",
        ]
        read_only_fields = ["id", "date_joined"]
        
    def to_internal_value(self, data):
        """
        Ignore date_joined s'il est envoyé dans la requête (protection)
        """
        if isinstance(data, dict) and 'date_joined' in data:
            data = data.copy()
            data.pop('date_joined', None)
        return super().to_internal_value(data)


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'admin avec plus de détails
    """
    date_joined = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "matricule",
            "nom",
            "prenom",
            "telephone",
            "date_joined",
            "is_member",
            "password_changed",
            "roles",
        ]
        read_only_fields = ["id", "date_joined"]
        
    def to_internal_value(self, data):
        """
        Ignore date_joined s'il est envoyé dans la requête (protection)
        """
        if isinstance(data, dict) and 'date_joined' in data:
            data = data.copy()
            data.pop('date_joined', None)
        return super().to_internal_value(data)

class UserRegisterationSerializer(serializers.ModelSerializer):


    class Meta:
        model = CustomUser
        fields = ["matricule","nom","prenom",'telephone',"password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            matricule=validated_data["matricule"],
            nom=validated_data["nom"],
            prenom=validated_data["prenom"],
            telephone=validated_data["telephone"],
            password=validated_data["password"]

        )

class UserLoginSerializer(serializers.Serializer):
    matricule = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(matricule=data["matricule"], password=data["password"])

        if user is None:
            raise serializers.ValidationError("Matricule ou mot de passe incorrect.")

        data["user"] = user
        return data

class AdminLoginSerializer(serializers.Serializer):
    matricule = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(matricule=data["matricule"], password=data["password"])

        if user is None:
            raise serializers.ValidationError("Identifiants incorrects.")

        # Seuls les utilisateurs ayant le rôle "admin" peuvent se connecter à l'interface admin
        if not user.roles.filter(type__iexact="admin").exists():
            raise serializers.ValidationError("Vous n'êtes pas autorisé.")

        data["user"] = user
        return data




