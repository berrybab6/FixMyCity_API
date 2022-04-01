from numpy import full
from rest_framework import serializers, fields
from .models import Role, Sector, SectorAdmin, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']
    
class SectorAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectorAdmin
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']

class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True)
    

class LoginSectorAdminSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.CharField(required=True)

    # def create(self, validated_data):
        # return User.objects.create(**validated_data)

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = "__all__"
        # extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']    
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ['id']    