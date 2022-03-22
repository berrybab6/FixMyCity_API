from django.contrib import admin
from .models import Sector, User, SectorAdmin , CustomUser , PhoneOTP
# # Register your models here.
admin.site.register(User)
admin.site.register(SectorAdmin)
admin.site.register(Sector)
admin.site.register(CustomUser)
admin.site.register(PhoneOTP)