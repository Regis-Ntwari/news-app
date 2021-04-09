from authentication.models import User
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    date_created = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

class ImageTest(models.Model):
    image = models.ImageField(upload_to='photos/')

