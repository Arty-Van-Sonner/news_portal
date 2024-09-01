# Generated by Django 4.2.15 on 2024-08-27 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(db_column='rating', default=0)),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('A', 'Article'), ('N', 'News')], db_column='type', max_length=1)),
                ('creation_date', models.DateTimeField(auto_now_add=True, db_column='creation_date')),
                ('title', models.CharField(db_column='title', max_length=255)),
                ('text', models.TextField(db_column='text')),
                ('rating', models.IntegerField(db_column='rating', default=0)),
                ('last_update_date', models.DateField(auto_now=True, db_column='last_update_date')),
                ('likes', models.PositiveIntegerField(db_column='likes', default=0)),
                ('dislikes', models.PositiveIntegerField(db_column='dislikes', default=0)),
                ('author', models.ForeignKey(db_column='author_id', on_delete=django.db.models.deletion.CASCADE, to='news.author')),
                ('category', models.ForeignKey(db_column='category_id', on_delete=django.db.models.deletion.CASCADE, to='news.category')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(db_column='category_id', on_delete=django.db.models.deletion.CASCADE, to='news.category')),
                ('post', models.ForeignKey(db_column='post_id', on_delete=django.db.models.deletion.CASCADE, to='news.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(db_column='text')),
                ('creation_date', models.DateTimeField(auto_now_add=True, db_column='creation_date')),
                ('rating', models.IntegerField(db_column='rating', default=0)),
                ('last_update_date', models.DateField(auto_now=True, db_column='last_update_date')),
                ('likes', models.PositiveIntegerField(db_column='likes', default=0)),
                ('dislikes', models.PositiveIntegerField(db_column='dislikes', default=0)),
                ('post', models.ForeignKey(db_column='post_id', on_delete=django.db.models.deletion.CASCADE, to='news.post')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
