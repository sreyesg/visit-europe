from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Comment(models.Model):
    content = models.TextField(max_length=250)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment_author.username} - {self.content[:20]}"   
    
class Article(models.Model):
    name = models.CharField(max_length=100)
    summary = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for article_id: {self.article_id}@{self.url}"