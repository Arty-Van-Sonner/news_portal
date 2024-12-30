from django.urls import path
# Импортируем созданное нами представление
from .views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/', PostDetail.as_view(), name='news_detail'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('articles/', ArticleList.as_view(), name='articles_list'),
    path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/', PostDetail.as_view(), name='articles_detail'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('post/search/', PostSearch.as_view(), name='post_search'), 
    path('post/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),  
]