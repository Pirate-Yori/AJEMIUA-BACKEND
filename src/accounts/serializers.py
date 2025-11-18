# users/serializers.py

from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"

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
    """
    Serializer class to authenticate users with email and password.
    """

    matricule = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

