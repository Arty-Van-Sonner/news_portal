from django.db import models

from django.contrib.auth.models import User

# Create your models here.
list_of_types_with_likes = []

class Author(models.Model):
    __user = models.ForeignKey(User, on_delete = models.CASCADE, db_column = 'user_id', name = 'user')
    __rating = models.IntegerField(default = 0, db_column = 'rating', name = 'rating')

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

class Category(models.Model):
    __name = models.CharField(max_length = 255, unique = True, db_column = 'name', name = 'name')

class Post(models.Model):
    __article = 'A'
    __news = 'N'
    __POST_TYPES = [
        (__article, 'Article'),
        (__news, 'News'),
    ]

    __author = models.ForeignKey(Author, on_delete = models.CASCADE, db_column = 'author_id', name = 'author')
    __type = models.CharField(max_length = 1, choices = __POST_TYPES, db_column = 'type', name = 'type')
    __creation_date = models.DateTimeField(auto_now_add = True, db_column = 'creation_date', name = 'creation_date')
    __category = models.ForeignKey(Category, on_delete = models.CASCADE, db_column = 'category_id', name = 'category')
    __title = models.CharField(max_length = 255, db_column = 'title', name = 'title')
    __text = models.TextField(db_column = 'text', name = 'text')
    __rating = models.IntegerField(default = 0, db_column = 'rating', name = 'rating')
    __last_update_date = models.DateTimeField(auto_now = True, db_column = 'last_update_date', name = 'last_update_date')
    __likes = models.PositiveIntegerField(default = 0, db_column = 'likes', name = 'likes')
    __dislikes = models.PositiveIntegerField(default = 0, db_column = 'dislikes', name = 'dislikes') 

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

class PostCategory(models.Model):
    __post = models.ForeignKey(Post, on_delete = models.CASCADE, db_column = 'post_id', name = 'post')
    __category = models.ForeignKey(Category, on_delete = models.CASCADE, db_column = 'category_id', name = 'category')

class Comment(models.Model):
    __post = models.ForeignKey(Post, on_delete = models.CASCADE, db_column = 'post_id', name = 'post')
    __user = models.ForeignKey(User, on_delete = models.CASCADE, db_column = 'user_id', name = 'user')
    __text = models.TextField(db_column = 'text', name = 'text')
    __creation_date = models.DateTimeField(auto_now_add = True, db_column = 'creation_date', name = 'creation_date')
    __rating = models.IntegerField(default = 0, db_column = 'rating', name = 'rating')
    __last_update_date = models.DateTimeField(auto_now = True, db_column = 'last_update_date', name = 'last_update_date')
    __likes = models.PositiveIntegerField(default = 0, db_column = 'likes', name = 'likes')
    __dislikes = models.PositiveIntegerField(default = 0, db_column = 'dislikes', name = 'dislikes')
    
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
