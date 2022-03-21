from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate



class RegistorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','phone_number')
        read_only_fields = ['id']
        

    def create(self, validated_data):
        user = User(first_name= validated_data['first_name'], last_name= validated_data['last_name'], phone_number= validated_data['phone_number'] )
        user.save()
        return user
    
    
    
class LoginUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    # password = serializers.CharField(
        # style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        # password = attrs.get('password')

        if phone_number:
            if User.objects.filter(phone_number=phone_number).exists():
                print("i am here")
                
                user = authenticate(request=self.context.get('request'),
                                    phone_number=phone_number)
                print(phone_number)
                
            else:
                msg = {'detail': 'Phone number is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    
    
class LoginSerializer(serializers.Serializer):
    # password = serializers.CharField(required=True, write_only=True)
    phone_number = serializers.CharField(required=True)

         
        