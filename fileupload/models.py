import os
from django.db import models
from uuid import uuid4

# Create your models here.
class Folder(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
def get_upload_path(instance, filename):
    return str(instance.folder.uid) +'/'+ filename
    
class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
