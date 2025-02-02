from django.shortcuts import render
from django.views.generic.edit import CreateView
from main_app.models import Article

def landing(request):
    return render(request,'base.html')



class ArticleCreate(CreateView):
    model = Article
    fields = '__all__'
    success_url = '/'
