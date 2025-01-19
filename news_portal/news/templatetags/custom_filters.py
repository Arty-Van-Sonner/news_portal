from django import template
from censor.censor import Censor
from news.models import Post

register = template.Library()

@register.filter
def censor(value):
    censor = Censor()
    censor.load_censor_words_from_file('censor/ban_words.txt')
    result = censor.hide_swear_words(str(value), "*")
    return result

@register.filter
def lower(value):
    return str(value).lower()

@register.filter
def get_absolute_url(post: Post):
    return post.get_absolute_url() 