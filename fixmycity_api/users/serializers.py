from rest_framework import serializers
from .models import User



class RegistorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','phone_number')
        read_only_fields = ['id']
        

    def create(self, validated_data):
        user = User(first_name= validated_data['first_name'], last_name= validated_data['last_name'], phone_number= validated_data['phone_number'] )
        user.save()
        return user
         
        