import uuid 
import boto3
import os
from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from main_app.models import Article, Photo
from django.http import Http404

class ArticleList(ListView):
    model = Article
    template_name = 'landing.html'
    context_object_name = 'articles'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_articles = Article.objects.all()
        unique_countries = Article.objects.values_list('country', flat=True).distinct()

        context['message'] = 'welcome to the app'
        context['countryset'] = unique_countries 
        
        return context

    # queryset = Article.objects.all()
    # countryset = Article.objects.values_list('country', flat=True).distinct()

class ArticleFilter(ListView):
    model = Article
    template_name = 'landing.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.GET.get('country')
        city = self.request.GET.get('city')

        if country:
            queryset = Article.objects.filter(country=country)
        if city:
            queryset = Article.objects.filter(city=city)
    
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_countries = Article.objects.values_list('country', flat=True).distinct()
        context['countryset'] = unique_countries         
        return context    

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


