from rest_framework import serializers

from .models import Role,CustomUser,RappelIslamique,Archive,Actualite,RessourceIslamique,UserRole,Evenement

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ('id','date_joined','roles',)

class RappelIslamiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RappelIslamique
        fields = '__all__'

class ActualiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actualite
        fields = '__all__'

class RessourceIslamiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RessourceIslamique
        fields = '__all__'

class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evenement
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'
