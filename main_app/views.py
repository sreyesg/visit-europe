import uuid 
import boto3
import os
from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, UpdateView, DeleteView, ListView

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



from main_app.models import Article, Photo, Comment
from .forms import CommentForm
from django.http import Http404
from django.urls import reverse_lazy


def signup(request):  
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


class ArticleList(ListView):  
    model = Article
    template_name = 'landing.html'
    context_object_name = 'articles'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        unique_countries = Article.objects.values_list('country', flat=True).distinct()
        unique_cities = Article.objects.values_list('city', flat=True).distinct()

        context['message'] = 'welcome to the app'
        context['countryset'] = unique_countries 
        context['cityset'] = unique_cities 
        
        return context

    
    

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
        unique_cities = Article.objects.values_list('city', flat=True).distinct()
        context['cityset'] = unique_cities         
        return context    


class ArticleDetail(DetailView):
    model = Article
    template_name = 'detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        article = self.get_object() 
        context['comments'] = Comment.objects.filter(article=article).order_by('-comment_author') 
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_author = request.user  
            comment.article = self.object
            comment.save()
            return redirect('article_detail', pk=self.object.pk)
        return self.get(request, *args, **kwargs)


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['name', 'summary','content','country','city']  

    def form_valid(self, form):

        form.instance.author = self.request.user 
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


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_update.html'
    
    def form_valid(self, form):
        form.instance.comment_author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.article.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.comment_author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.article.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.comment_author
