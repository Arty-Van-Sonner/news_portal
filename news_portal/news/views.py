from django.shortcuts import render

from django.views.generic import *
from .models import *
from django.shortcuts import get_object_or_404


class NewsList(ListView):
    '''
    
    '''
    model = Post
    context_object_name = 'news'
    template_name = 'news/news_list.html'

    def get_queryset(self):
        return Post.objects.filter(type = 'N').order_by('-creation_date')

class NewsDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'news/news_detail.html'

# class PostCreat(CreateView):
#     model = Post
#     fields = '__all__'

# class MyForm(FormView):
#     # form_class = myform
#     success_url = '/success/'
    
#     def form_valid(self, form):
#         return super().form_invalid(form)
