from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter, DateFromToRangeFilter, CharFilter, ChoiceFilter
from .models import *
from django.forms.widgets import TextInput, Select, DateTimeInput

class NewFilter(FilterSet):
    title = CharFilter(
        field_name = 'title',
        lookup_expr = 'icontains',
        label = 'Title',
        widget = TextInput(attrs = {'class': 'form-control'})
    )
    category = ModelChoiceFilter(
        field_name = 'category',
        queryset = Category.objects.all(),
        lookup_expr = 'exact',
        label = 'Category',
        widget = Select(attrs = {'class': 'form-select'})
    )
    creation_date = DateTimeFilter(
        field_name = 'creation_date',
        label = 'Creation date',
        widget = DateTimeInput(
            attrs={ 
                'class': 'form-control', 
                'type': 'datetime-local',
            }
        ),
        lookup_expr = 'gt',
    )
    
    class Meta:
        model = Post
        fields = {}

class PostFilter(NewFilter):
    type = ChoiceFilter(
        field_name = 'type',
        choices = Post.POST_TYPES,
        lookup_expr = 'exact',
        label = 'Type',
        widget = Select(attrs = {'class': 'form-select'})
    )
