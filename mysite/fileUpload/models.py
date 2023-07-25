from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ImageModel(models.Model):
    files = models.ImageField('첨부 파일', upload_to='uploads/')
    desc = models.CharField(max_length=512)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
