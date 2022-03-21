from rest_framework import serializers
from .models import Announcement
from accounts.serializers import SectorSerializer


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"
        # depth = 1
        


