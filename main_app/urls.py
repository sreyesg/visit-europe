from django.urls import path
from . import views
from main_app.views import ArticleCreate, ArticleDetail, ArticleUpdate

urlpatterns = [
    path('', views.Landing.as_view(), name='landing'),
    path('articles/create/', views.ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('articles/<int:pk>/update/', views.ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', views.ArticleDelete.as_view(), name='article_delete'),
    path('accounts/signup/', views.signup, name='signup'),  
    path('articles/<int:article_id>/add_photo', views.add_photo, name='add_photo'),   
]
