from numpy import full
from rest_framework import serializers, fields
from .models import SectorAdmin, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']
    
    # def create(self, validated_data):
    #     if validated_data.get('image'):
    #         user = User(username= validated_data['username'], full_name= validated_data['full_name'], image= validated_data['image'] )
    #     else:
    #         user = User(username= validated_data['username'], full_name = validated_data['full_name'])

    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
class SectorAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectorAdmin
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']

class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True)