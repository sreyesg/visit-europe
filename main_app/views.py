import uuid 
import boto3
import os
from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth.views import LoginView

from main_app.models import Article, Photo


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('article_create')
        else:
            error_message = 'Invalid Signup'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)


class Landing(LoginView):
    template_name = 'landing.html'
    
class ArticleDetail(DetailView):
    model = Article
    template_name = 'detail.html'
    context_object_name = 'article'

class ArticleCreate(CreateView):
    model = Article
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user  
        
        return super().form_valid(form)

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


