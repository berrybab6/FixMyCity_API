from django.db import models
from accounts.models import Sector , SectorAdmin



class Announcement(models.Model):
    id          = models.AutoField(primary_key=True)
    sector      = models.ForeignKey(Sector, on_delete=models.CASCADE , null=True)
    sectoradmin = models.ForeignKey(SectorAdmin, on_delete=models.CASCADE , null=True)
    title       = models.CharField(max_length = 255, null = True)
    description = models.CharField(max_length = 255, null = True)
    date        = models.DateTimeField(auto_now=True ,null=True )
    image       = models.CharField(max_length = 255, null = True)
   
    def __str__(self):
        return self.title
    
    
    


   

