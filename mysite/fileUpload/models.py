from django.db import models


# Create your models here.

class ImageModel(models.Model):
    files = models.ImageField('첨부 파일', upload_to='uploads/')
    desc = models.CharField(max_length=512)
