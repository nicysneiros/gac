from django.db import models

# Create your models here.


class Draft(models.Model):

	name = models.CharField(max_length=100)

	photo = models.ImageField(upload_to='fotos/', max_length = 1024)