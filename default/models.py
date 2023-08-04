from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save

# Create your models here.
class Services(models.Model):
    name = models.CharField(max_length=300, default="")
    
    def __str__(self):
        return self.name
    
class Hospital(models.Model):
    location = models.CharField(max_length=300, default="")
    name = models.CharField(max_length=300, default="")
    services = models.ManyToManyField(Services)
    working_hours = models.CharField(max_length=100, default="")
    status_open = models.BooleanField(default=True)
    cover = models.ImageField(upload_to="hospitals/", default="/hospitals/default.png")
    
    def __str__(self):
        return self.name
    
class PatientProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_id = models.CharField(default="", max_length=300)
    location = models.CharField(default="", max_length=300)
    
    def __str__(self):
        return self.patient_id

    #def created_user_profile(sender, instance, created, **kwargs):
        #if created:
            #PatientProfile.objects.create(user=instance)
    #post_save.connect(created_user_profile, sender=User)        
