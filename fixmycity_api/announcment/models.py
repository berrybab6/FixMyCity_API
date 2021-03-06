from django.db import models
from accounts.models import Sector , User
from cloudinary.models import CloudinaryField



class Announcement(models.Model):
    id          = models.AutoField(primary_key=True)
    sector      = models.ForeignKey(Sector, on_delete=models.CASCADE , null=True)
    sectoradmin = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    title       = models.CharField(max_length = 255, null = True)
    description = models.CharField(max_length = 255, null = True)
    createdAt    = models.DateTimeField(auto_now_add=True , null=True)
    updatedAt  = models.DateTimeField(auto_now=True ,null=True )
    image       = CloudinaryField('image' , null=True , blank=True)
    
   
    def __str__(self):
        return self.title
    
    
    


   

