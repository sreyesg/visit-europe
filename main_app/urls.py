from django.urls import path
from . import views
from main_app.views import ArticleCreate, ArticleList

urlpatterns = [
    path('', views.ArticleList.as_view(), name='landing'),
    path('articles/create', views.ArticleCreate.as_view(), name='article_create'),
]
