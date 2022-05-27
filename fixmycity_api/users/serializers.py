from rest_framework import serializers
from accounts.models import PhoneOTP, User , Role



class RegistorUserSerializer(serializers.ModelSerializer):
    class Meta:

        model = User
        fields = ( 'id', 'first_name', 'last_name','phone_number' , 'ProfileImage')

        read_only_fields = ['id']
        

    def create(self, validated_data):
        role = Role.objects.get(id=3)
        user = User(first_name= validated_data['first_name'], last_name= validated_data['last_name'], phone_number= validated_data['phone_number'] , roles = role )
        user.save()
        return user
    
    
    

    
class LoginSerializer(serializers.ModelSerializer):
    ProfileImage = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    phone_number = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ("id","phone_number" , 'first_name' , 'last_name' , 'ProfileImage')
    # first_name = serializers.CharField(required=True)
    # last_name = serializers.CharField(required=True)
    # ProfileImage = serializers.CharField(required = False)
    
    
class UpdateUserSerializer(serializers.ModelSerializer):
    ProfileImage = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = User
        fields = ('ProfileImage',)
        read_only_fields = ('id' , 'phone_number' , 'first_name' , 'last_name',)  
        
        
class ValidatePhoneSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = PhoneOTP
        fields = ('phone_number',)
        
        
class ValidateOtpSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = PhoneOTP
        fields = ('phone_number', 'otp')
       
       
      