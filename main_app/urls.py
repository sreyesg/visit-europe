from django.urls import path
from . import views
from main_app.views import ArticleCreate

urlpatterns = [
    path('', views.landing, name='landing'),
    path('articles/create', views.ArticleCreate.as_view(), name='article_create'),
]
