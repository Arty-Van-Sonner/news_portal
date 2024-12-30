from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import render

from django.urls import reverse_lazy
from django.http.request import QueryDict

from django.views.generic import *
from .models import *
from django.shortcuts import get_object_or_404

from .forms import *

from .filters import *
import inspect
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# from django.forms.widgets import 

class NewsList(ListView):
    '''
    
    '''
    model = Post
    context_object_name = 'post'
    template_name = 'news/post_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(type = 'N')
        return queryset

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['form_title'] = 'News'
       context['post_update'] = 'news_update'
       context['post_delete'] = 'news_delete'
       context['posts_list_is_empty'] = 'There is no news'
       return context

class ArticleList(ListView):
    '''
    
    '''
    model = Post
    context_object_name = 'post'
    template_name = 'news/post_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(type = 'A')
        return queryset

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['form_title'] = 'Articles'
       context['post_update'] = 'articles_update'
       context['post_delete'] = 'articles_delete'
       context['posts_list_is_empty'] = 'There is no articles'
       return context

class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'news/post_detail.html'

class NewsSearch(ListView):
    model = Post
    context_object_name = 'news'
    template_name = 'news/news_search.html'
    queryset_is_empty = True
    parameters_are_set = False

    def get_queryset(self): 
        return self.processing_queryset(filter_class = NewFilter, type = 'N')

    def processing_queryset(self, filter_class, **kwargs):
        parametrs = self.request.GET.copy()
        queryset = Post.objects.none()
        if len(parametrs) > 0:
            if len(kwargs) == 0:
                queryset = Post.objects.all()
            else:
                queryset = Post.objects.filter(**kwargs)
            self.parameters_are_set = True
        else:
            self.parameters_are_set = False
        self.filterset = filter_class(self.request.GET, queryset)
        queryset = self.filterset.qs
        if len(queryset) == 0:
            self.queryset_is_empty = True
        else:
            self.queryset_is_empty = False
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['queryset_is_empty'] = self.queryset_is_empty
        context['parameters_are_set'] = self.parameters_are_set
        return context

class PostSearch(NewsSearch):
    '''
    '''
    # filter_class = PostFilter  
    def get_queryset(self):
        return super().processing_queryset(filter_class = PostFilter)

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = NewsForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news/post_edit.html'
    # context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create new news'
        return context

class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = ArticleForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news/post_edit.html'
    # context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create new article'
        return context

# Добавляем представление для изменения товара.
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'{ context["post"].title } (edit)'
        return context

# Представление удаляющее товар.
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Delete {context["post"].title}?'
        return context
