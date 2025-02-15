import uuid 
import boto3
import os
from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, UpdateView, DeleteView, ListView

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



from main_app.models import Article, Photo
from django.http import Http404


def signup(request):  # added signup 
    error_message = ''
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

def user_login(request):
    error_message = ''
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password) 
            if user is not None:
                login(request, user) 
                return redirect('article-index') 
            else:
                error_message = 'Invalid login credentials' 
        else:
            error_message = 'Invalid login - try again' 

    form = AuthenticationForm() 
    context = {'form': form, 'error_message': error_message}
    return render(request, 'login.html', context) 

@login_required
def article_index(request):

    articles = Article.objects.filter(author=request.user)

    return render(request, 'articles/index.html', {'articles': articles})


class ArticleList(LoginView):  #(ListView)
    model = Article
    template_name = 'landing.html'
    context_object_name = 'articles'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_articles = Article.objects.all()
        unique_countries = Article.objects.values_list('country', flat=True).distinct()
        unique_cities = Article.objects.values_list('city', flat=True).distinct()

        context['message'] = 'welcome to the app'
        context['countryset'] = unique_countries 
        context['cityset'] = unique_cities 
        
        return context

    # queryset = Article.objects.all()
    # countryset = Article.objects.values_list('country', flat=True).distinct()

class ArticleFilter(LoginView): #ListView
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
        unique_cities = Article.objects.values_list('city', flat=True).distinct()
        context['cityset'] = unique_cities         
        return context    


class ArticleDetail(DetailView):
    model = Article
    template_name = 'detail.html'
    context_object_name = 'article'

class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    fields = '__all__'
    def form_valid(self, form):

        form.instance.user = self.request.user
        return super().form_valid(form)

class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ['summary','content','country','city']


class ArticleDelete(LoginRequiredMixin, DeleteView):
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


