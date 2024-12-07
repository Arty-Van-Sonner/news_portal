from django.urls import path
# Импортируем созданное нами представление
from .views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('news/', NewsList.as_view()),
    path('news/<int:pk>/', NewsDetail.as_view()),   
]