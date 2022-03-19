from django.contrib import admin
from .models import Sector, User, SectorAdmin
# # Register your models here.
admin.site.register(User)
admin.site.register(SectorAdmin)
admin.site.register(Sector)