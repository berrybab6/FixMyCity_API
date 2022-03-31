
from rest_framework import serializers
from accounts.models import CustomUser , Role
from django.contrib.auth import authenticate



class RegistorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','phone_number' , 'ProfileImage')
        read_only_fields = ['id']
        

    def create(self, validated_data):
        role = Role.objects.get(id=3)
        user = CustomUser(first_name= validated_data['first_name'], last_name= validated_data['last_name'], phone_number= validated_data['phone_number'] ,ProfileImage = validated_data['ProfileImage'], roles = role )
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
            if CustomUser.objects.filter(phone_number=phone_number).exists():
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
    
    
class LoginSerializer(serializers.ModelSerializer):
    ProfileImage = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    phone_number = serializers.CharField(required=True)
    class Meta:
        model = CustomUser
        fields = ("phone_number" , 'first_name' , 'last_name' , 'ProfileImage')
    # first_name = serializers.CharField(required=True)
    # last_name = serializers.CharField(required=True)
    # ProfileImage = serializers.CharField(required = False)

         
        