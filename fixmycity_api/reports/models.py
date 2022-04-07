from venv import create
from django.contrib.gis.db import models
from accounts.models import Sector, upload_to
from accounts.models import CustomUser
from django.contrib.postgres.fields import ArrayField
from django_filters import FilterSet

from django_filters import DateTimeFromToRangeFilter 

# class Location(models.Model):
#     id              = models.AutoField(primary_key=True)
#     longitude       = models.FloatField()
#     latitude        = models.FloatField()
#     cityName        = models.CharField(max_length = 255, null= True)
   
#     def __str__(self):
#         return str(self.cityName)







class Report(models.Model):
    id          = models.AutoField(primary_key=True)
    user      = models.ForeignKey(CustomUser, on_delete=models.CASCADE , null=True)
    sector    = models.ForeignKey(Sector, on_delete=models.CASCADE , null=True)
    image       = models.ImageField(upload_to="reports"  , null=True , blank=True)
    tag         = ArrayField(models.CharField(max_length=200), blank=True , null=True)
    description = models.CharField(max_length = 255, null = True)
    postedAt    = models.DateTimeField(auto_now=True , null=True)
    resolvedAt  = models.DateTimeField(auto_now=True ,null=True )
    noOfLikes   = models.ManyToManyField(CustomUser , related_name='report_posts')
    spamStatus  = models.BooleanField(default=False)
    state       = models.BooleanField(default=False)
    location    =  models.PointField(null=True, blank=True,)
    
    
    def __str__(self):
        return self.description
    
    
    def number_of_likes(self):
        return self.noOfLikes.count()
    
    
class F(FilterSet):
    postedAt = DateTimeFromToRangeFilter()

    class Meta:
        model = Report
        fields = ['postedAt']


   

