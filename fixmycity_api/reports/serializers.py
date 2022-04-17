from rest_framework import serializers
from .models import Report
from accounts.models import Sector , CustomUser
from accounts.serializers import SectorSerializer
from users.serializers import RegistorUserSerializer


class ReportSerializer(serializers.ModelSerializer):
    
    distance = serializers.DecimalField(source="distance.m" , max_digits=100 , decimal_places=2 , required= False , read_only = True)
    like_count = serializers.SerializerMethodField()
    class Meta:
        model = Report
        fields = ("id" ,"image", "tag", "description",  "postedAt" ,"distance" , "like_count" , "sector", "user", "location" ,'state' , 'spamStatus' )
        read_only_fields = ("id" , "distance")
        # fields = "__all__"
        
    def get_like_count(self, obj):
        return obj.noOfLikes.count()
   
    
        
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            sector = Sector.objects.get(pk=data['sector'])
            data['sector'] = SectorSerializer(sector).data
        except Sector.DoesNotExist:
            sector = None
        
        try:
            user = CustomUser.objects.get(pk=data['user'])
            data['user'] = RegistorUserSerializer(user).data
            
        except CustomUser.DoesNotExist:
            user = None
        
        return data  
    

class ReportUpdateSerializer(serializers.ModelSerializer):
   class Meta:
        model = Report
        fields = ('id' , 'sector' ,'state' , 'spamStatus' )
        read_only_fields = ("id" ,"image", "tag", "description",  "postedAt" ,"distance" , "like_count" , "sector", "user", "location"  )
        # fields = "__all__"
          
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ("location",)
    

# class LocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location
#         fields = "__all__"