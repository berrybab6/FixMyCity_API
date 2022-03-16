from numpy import full
from rest_framework import serializers, fields
from .models import SuperAdmin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['id', 'password','full_name', 'profile_pic','username','image']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']
    
    def create(self, validated_data):
        if validated_data.get('image'):
            user = SuperAdmin(username= validated_data['username'], full_name= validated_data['full_name'], image= validated_data['image'] )
        else:
            user = SuperAdmin(username= validated_data['username'], full_name = validated_data['full_name'])

        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True)