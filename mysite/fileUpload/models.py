from django.db import models
from django.contrib.auth.models import User
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible


# Create your models here.


@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


class ImageModel(models.Model):
    files = models.ImageField('첨부 파일', 
        upload_to=UploadToPathAndRename('uploads'))
    desc = models.CharField(max_length=512)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    result = models.CharField(max_length=512)





