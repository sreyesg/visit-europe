from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from main_app.models import Article

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
