from venv import create
from django.contrib.gis.db import models
from accounts.models import Sector, upload_to
from accounts.models import User
from django.contrib.postgres.fields import ArrayField
from django_filters import FilterSet
from django_filters import DateTimeFromToRangeFilter 
from cloudinary.models import CloudinaryField








class Report(models.Model):
    STATUS_CHOICES = (
                        ('RESOLVED' , 'RESOLVED'),
                        ('UNRESOLVED' , 'UNRESOLVED'),
                        ('REJECTED' , 'REJECTED')
                     )

    id          = models.AutoField(primary_key=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    sector      = models.ForeignKey(Sector, on_delete=models.CASCADE , null=True)
    image       = CloudinaryField('image' , null=True , blank= True)
    tag         = ArrayField(models.CharField(max_length=200), blank=True , null=True)
    description = models.CharField(max_length = 255, null = True)
    postedAt    = models.DateTimeField(auto_now_add=True , null=True)
    resolvedAt  = models.DateTimeField(auto_now=True ,null=True )
    noOfLikes   = models.ManyToManyField(User , related_name='report_posts')
    spamStatus  = models.BooleanField(default=False)
    state       = models.BooleanField(default=False) #state is for seen and unseen report
    status      = models.CharField(max_length=100, choices=STATUS_CHOICES , default='UNRESOLVED')
    location    = models.PointField(null=True, blank=True,)
    latitude    = models.CharField(null=True , blank=True , max_length=255)
    longtiude   = models.CharField(null=True , blank=True , max_length=255)
    
    
    def __str__(self):
        return self.description
    
    
    def number_of_likes(self):
        return self.noOfLikes.count()
    
    
class F(FilterSet):
    postedAt = DateTimeFromToRangeFilter()

    class Meta:
        model = Report
        fields = ['postedAt']


   

