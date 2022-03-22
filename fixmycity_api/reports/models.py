from django.db import models
from accounts.models import Sector
from accounts.models import CustomUser
from django.contrib.postgres.fields import ArrayField



class Location(models.Model):
    id              = models.AutoField(primary_key=True)
    longitude       = models.FloatField()
    latitude        = models.FloatField()
    cityName        = models.CharField(max_length = 255, null= True)
   
    def __str__(self):
        return str(self.cityName)







class Report(models.Model):
    id          = models.AutoField(primary_key=True)
    userId      = models.ForeignKey(CustomUser, on_delete=models.CASCADE , null=True)
    sectorId    = models.ForeignKey(Sector, on_delete=models.CASCADE , null=True)
    image       = models.CharField(max_length = 255  , null=True , blank=True)
    tag         = ArrayField(models.CharField(max_length=200), blank=True)
    description = models.CharField(max_length = 255, null = True)
    postedAt    = models.DateTimeField(auto_now=True , null=True)
    resolvedAt  = models.DateTimeField(auto_now=True ,null=True )
    noOfLikes   = ArrayField(models.IntegerField(default=0), blank=True , null=True )
    spamStatus  = models.BooleanField(default=False)
    state       = models.BooleanField(default=False)
    location    = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.description
    
    
    


   

