from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from main_app.models import Article

class ArticleList(ListView):
    model = Article
    template_name = 'lading.html'
    context_object_name = 'articles'
    queryset = Article.objects.all()
    


class ArticleCreate(CreateView):
    model = Article
    fields = '__all__'
    success_url = '/'
