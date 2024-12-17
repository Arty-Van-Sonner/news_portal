from django.forms import ModelForm, CharField, ModelChoiceField, ChoiceField
from django.forms.widgets import Textarea, TextInput, Select
from .models import *

class PostForm(ModelForm):
    title = CharField(
        widget = TextInput(
            attrs={ 
                'class': 'form-control', 
            }
        )
    )
    author = ModelChoiceField(
        queryset = Author.objects.all(),
        widget = Select(
            attrs={ 
                'class': 'form-select', 
            }
        )
    )
    category = ModelChoiceField(
        queryset = Category.objects.all(),
        widget = Select(
            attrs={ 
                'class': 'form-select', 
            }
        )
    )
    text = CharField(
        widget = Textarea(
            attrs={ 
                'class': 'form-control', 
            }
        )
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'category',
            'text',
            'type',
        ]

class NewsForm(PostForm):
    '''
    '''
    type = CharField(
        label = '',
        widget = TextInput(
            attrs={ 
                'class': 'form-control', 
                'type': 'hidden',
                'value': Post.POST_TYPES[1][0],
            }
        )
    )

class ArticleForm(PostForm):
    '''
    '''
    type = CharField(
        label = '',
        widget = TextInput(
            attrs={ 
                'class': 'form-control', 
                'type': 'hidden',
                'value': Post.POST_TYPES[0][0],
            }
        )
    )