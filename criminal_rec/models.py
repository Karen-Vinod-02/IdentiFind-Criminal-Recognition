import os
from django.db import models
from django.utils import timezone

# Custom upload path function for the 'front/' directory
def upload_to_front(instance, filename):
    return os.path.join('front', filename)

class CriminalRec(models.Model):
    criminal_id = models.CharField(primary_key=True, max_length=20)
    criminal_name = models.CharField(max_length=255)  
    criminal_photo = models.ImageField(upload_to='front/', blank=True, null=True)  # Criminal's photo in 'front/'
    captured_image = models.ImageField(upload_to='captured_images/', blank=True, null=True)  # Image captured from user
    description = models.TextField(blank=True, null=True)  
    scars_or_marks = models.TextField(blank=True, null=True)  
    crime = models.TextField(blank=True, null=True)   
    parole_status = models.TextField(blank=True, null=True)  
    parent_institution = models.CharField(max_length=255, blank=True, null=True)  
    uploaded_at = models.DateTimeField(default=timezone.now)  
    authorized = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.criminal_name} - {self.description}"

class CameraConfiguration(models.Model):
    name = models.CharField(max_length=255)
    camera_source = models.CharField(max_length=255)  # Can be a URL or device index (e.g., "0" or "http://...")
    threshold = models.FloatField(default=0.8)  # Detection threshold

    def __str__(self):
        return self.name