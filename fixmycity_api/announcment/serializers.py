from rest_framework import serializers
from .models import Announcement
from accounts.serializers import SectorSerializer


class AnnouncementSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
   
    class Meta:
        model = Announcement
        fields = "__all__"
        # depth = 1
        
        


