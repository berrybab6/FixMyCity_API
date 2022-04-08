from numpy import full
from rest_framework import serializers, fields
from .models import Sector, User , Role


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']
        
        
        
        
        
        
        
    
class SectorAdminSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(
    #     max_length=68, min_length=6, write_only=True)

    # default_error_messages = {
    #     'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['email' , 'roles' , 'sector']
        
    def create(self, validated_data):
        role = Role.objects.get(id=2)
        user = User(email= validated_data['email'],roles = role , sector = validated_data['sector'] )
        user.save()
        return user

    # def validate(self, attrs):
    #     email = attrs.get('email' )
    #     raise serializers.ValidationError(
    #     self.default_error_messages)
        # username = attrs.get('username', '')

        # if not username.isalnum():
        #     raise serializers.ValidationError(
        #         self.default_error_messages)
        # return attrs

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)

   
    
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']
    
    
    
    
    
    
    
    
    

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