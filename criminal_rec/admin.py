from django.contrib import admin
from .models import CriminalRec, CameraConfiguration

@admin.register(CriminalRec)
class CriminalRecAdmin(admin.ModelAdmin):
    list_display = ['criminal_id','criminal_photo','criminal_name', 'description', 'authorized', 'parole_status', 'parent_institution', 'uploaded_at','scars_or_marks']
    search_fields = ['criminal_name', 'description', 'parent_institution']
    list_filter = ['authorized']  
    readonly_fields = ['captured_image'] # Make captured_image read-only in admin

@admin.register(CameraConfiguration)
class CameraConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'camera_source', 'threshold']
    search_fields = ['name', 'camera_source']