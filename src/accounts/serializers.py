# users/serializers.py

from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer pour les utilisateurs (exclut le mot de passe)
    """
    class Meta:
        model = CustomUser
        fields = ["id", "matricule", "nom", "prenom", "telephone", "email", 
                  "date_joined", "is_member", "is_admin", "is_active", "is_staff", "roles"]
        read_only_fields = ["id", "date_joined"]


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'admin avec plus de détails
    """
    class Meta:
        model = CustomUser
        fields = ["id", "matricule", "nom", "prenom", "telephone", "email", 
                  "date_joined", "is_member", "is_admin", "is_active", "is_staff", "roles"]
        read_only_fields = ["id", "date_joined"]

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

        if not user.is_admin:
            raise serializers.ValidationError("Vous n'êtes pas autorisé.")

        data["user"] = user
        return data




