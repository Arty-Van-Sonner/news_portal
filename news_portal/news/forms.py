from django.forms import ModelForm, CharField, ModelChoiceField, ChoiceField
from django.forms.widgets import Textarea, TextInput, Select
from django.core.exceptions import ValidationError
from .models import *

class PostForm(ModelForm):
    title = CharField(
        min_length=1,
        widget = TextInput(
            attrs={ 
                'class': 'form-control', 
            }
        ),
    )
    author = ModelChoiceField(
        queryset = Author.objects.all(),
        widget = Select(
            attrs={ 
                'class': 'form-select', 
            }
        ),
    )
    category = ModelChoiceField(
        queryset = Category.objects.all(),
        widget = Select(
            attrs={ 
                'class': 'form-select', 
            }
        ),
    )
    text = CharField(
        min_length=1,
        widget = Textarea(
            attrs={ 
                'class': 'form-control', 
            }
        ),
    )

    def clean_author(self):
        author = self.cleaned_data["author"]
        if type(author) != int and type(author) != Author:
            raise ValidationError(
                "Author must be filled!"
            )
        return author

    def clean_category(self):
        category = self.cleaned_data["category"]
        if type(category) != int and type(category) != Category:
            raise ValidationError(
                "Category must be filled!"
            )
        return category

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