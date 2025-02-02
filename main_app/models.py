from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    content = models.TextField(max_length=250)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Article(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(max_length=250)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name
    
# Create your models here.
