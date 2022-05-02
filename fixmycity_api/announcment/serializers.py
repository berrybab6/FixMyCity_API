from rest_framework import serializers
from .models import Announcement
from accounts.serializers import SectorSerializer , SectorAdminSerializer
from accounts.models import Sector , User



class AnnouncementSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    
    class Meta:
        model = Announcement
        fields = "__all__"
        # depth = 1
        
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            sector = Sector.objects.get(pk=data['sector'])
            data['sector'] = SectorSerializer(sector).data
        except Sector.DoesNotExist:
            sector = None
        
        try:
            sectoradmin = User.objects.get(pk=data['sectoradmin'])
            data['sectoradmin'] = SectorAdminSerializer(sectoradmin).data
            
        except User.DoesNotExist:
            sectoradmin = None
        
        return data
        
        


