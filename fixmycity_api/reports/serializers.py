from rest_framework import serializers
from .models import Location, Report
from accounts.models import Sector , CustomUser
from accounts.serializers import SectorSerializer
from users.serializers import RegistorUserSerializer


class ReportSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    class Meta:
        model = Report
        fields = "__all__"
        
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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"