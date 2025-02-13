import uuid 
import boto3
import os
from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from main_app.models import Article, Photo

class ArticleList(ListView):
    model = Article
    template_name = 'landing.html'
    context_object_name = 'articles'
    queryset = Article.objects.all()
    
class ArticleDetail(DetailView):
    model = Article
    template_name = 'detail.html'
    context_object_name = 'article'

class ArticleCreate(CreateView):
    model = Article
    fields = '__all__'
    success_url = '/'

class ArticleUpdate(UpdateView):
    model = Article
    fields = ['summary','content','country','city']


class ArticleDelete(DeleteView):
    model = Article
    success_url = '/'

def add_photo(request, article_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file,bucket,key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, article_id=article_id)
        except Exception as e:
            print('An error occured uploading file to S3')
            print(e)
    
    return redirect('article_detail', pk=article_id)


