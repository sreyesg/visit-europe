from django.urls import path
from . import views
from main_app.views import ArticleCreate, ArticleDetail, ArticleList, ArticleUpdate

urlpatterns = [
    path('', views.ArticleList.as_view(), name='landing'),
    path('articles/create', views.ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>', views.ArticleDetail.as_view(), name='article_detail'),
    path('articles/<int:pk>/update', views.ArticleUpdate.as_view(), name='article_update'),
    # path('articles/delete', views.ArticleDelete.as_view(), name='article_Delete'),

]
