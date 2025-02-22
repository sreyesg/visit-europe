from django.urls import path
from . import views
from main_app.views import ArticleCreate, ArticleDetail, ArticleList, ArticleUpdate, ArticleFilter, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('', views.ArticleList.as_view(), name='landing'),
    path('articles/index', views.article_index, name='article-index'),
    path('articles/create/', views.ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('articles/<int:pk>/update/', views.ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', views.ArticleDelete.as_view(), name='article_delete'),
    path('articles/<int:article_id>/add_photo', views.add_photo, name='add_photo'),   
    path('articles/', views.ArticleFilter.as_view(), name='article_filter'),

    path('accounts/login/', views.user_login, name='login'),
    path('accounts/signup/', views.signup, name='signup'),

    path('comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

]
