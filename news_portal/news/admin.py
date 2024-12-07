from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(CustomUser)
# admin.site.register(Comment)
