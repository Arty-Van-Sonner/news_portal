from django.db import models

from django.contrib.auth.models import User

from django.urls import reverse
# import SQLAlchemy

# Create your models here.
list_of_types_with_likes = []

class CustomUser(models.Model):
    male = 'm'
    female = 'f'
    GENDERS = [
        (male, 'male (man)'),
        (female, 'female (woman)'),
    ]
    
    user = models.ForeignKey(User, on_delete = models.CASCADE, unique = True, db_column = 'user_id', name = 'user')
    name = models.CharField(max_length = 128, db_column = 'name', name = 'name')
    family = models.CharField(max_length = 128, db_column = 'family', name = 'family')
    age = models.IntegerField(default = 0, db_column = 'age', name = 'age')
    gender = models.CharField(max_length = 1, choices = GENDERS, db_column = 'gender', name = 'gender')

class Author(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, db_column = 'custom_user_id', name = 'custom_user')
    rating = models.IntegerField(default = 0, db_column = 'rating', name = 'rating')

    def update_rating(self, save_object = True):
        posts = Post.objects.filter(author = self)
        comments = Comment.objects.filter(user = self.user)
        posts_comments = Comment.objects.filter(post__in = posts)
        raiting_of_posts = posts.values('rating')
        raiting_of_comments = comments.values('rating')
        raiting_of_posts_comments = posts_comments.values('rating')
        raiting_summ = 0
        for element in raiting_of_posts.values():
            raiting_summ += element['rating']
        raiting_summ *= 3
        for element in raiting_of_comments.values():
            raiting_summ += element['rating']
        for element in raiting_of_posts_comments.values():
            raiting_summ += element['rating'] 
        self.rating = raiting_summ
        if save_object:
            self.save()

    def __str__(self) -> str:
        name = self.custom_user.name[0]
        family = self.custom_user.family
        return f'{family} {name}.'

class Category(models.Model):
    name = models.CharField(max_length = 255, unique = True, db_column = 'name', name = 'name')

    def __str__(self) -> str:
        return f'{self.name} ({self.id})'

class Post(models.Model):
    article = 'A'
    news = 'N'
    POST_TYPES = [
        (article, 'Article'),
        (news, 'News'),
    ]

    author = models.ForeignKey(Author, on_delete = models.CASCADE, db_column = 'author_id', name = 'author')
    type = models.CharField(max_length = 1, choices = POST_TYPES, db_column = 'type', name = 'type')
    creation_date = models.DateTimeField(auto_now_add = True, db_column = 'creation_date', name = 'creation_date')
    category = models.ForeignKey(Category, on_delete = models.CASCADE, db_column = 'category_id', name = 'category')
    title = models.CharField(max_length = 255, db_column = 'title', name = 'title')
    text = models.TextField(db_column = 'text', name = 'text')
    rating = models.IntegerField(default = 0, db_column = 'rating', name = 'rating')
    last_update_date = models.DateTimeField(auto_now = True, db_column = 'last_update_date', name = 'last_update_date')
    likes = models.PositiveIntegerField(default = 0, db_column = 'likes', name = 'likes')
    dislikes = models.PositiveIntegerField(default = 0, db_column = 'dislikes', name = 'dislikes') 

    def like(self, save = True):
        self.__like_dislike(True)
        if save:
            self.save()

    def dislike(self, save = True):
        self.__like_dislike(False)
        if save:
            self.save()

    def __like_dislike(self, like):
        if like:
            self.likes += 1
            self.rating += 1
        else:
            self.dislikes += 1
            self.rating -= 1

    def preview(self):
        return self.text[:124] + '...'

    def get_absolute_url(self):
        if self.type == self.POST_TYPES[0][0]:
            return reverse('articles_detail', args=[str(self.id)])
        else:
            return reverse('news_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, db_column = 'post_id', name = 'post')
    category = models.ForeignKey(Category, on_delete = models.CASCADE, db_column = 'category_id', name = 'category')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, db_column = 'post_id', name = 'post')
    user = models.ForeignKey(User, on_delete = models.CASCADE, db_column = 'user_id', name = 'user')
    text = models.TextField(db_column = 'text', name = 'text')
    creation_date = models.DateTimeField(auto_now_add = True, db_column = 'creation_date', name = 'creation_date')
    rating = models.IntegerField(default = 0, db_column = 'rating', name = 'rating')
    last_update_date = models.DateTimeField(auto_now = True, db_column = 'last_update_date', name = 'last_update_date')
    likes = models.PositiveIntegerField(default = 0, db_column = 'likes', name = 'likes')
    dislikes = models.PositiveIntegerField(default = 0, db_column = 'dislikes', name = 'dislikes')
    
    def like(self, save = True):
        self.__like_dislike(True)
        if save:
            self.save()

    def dislike(self, save = True):
        self.__like_dislike(False)
        if save:
            self.save()

    def __like_dislike(self, like):
        if like:
            self.likes += 1
            self.rating += 1
        else:
            self.dislikes += 1
            self.rating -= 1

list_of_types_with_likes.append(Post)
list_of_types_with_likes.append(Comment)
