from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from django.contrib.auth.models import User


class Tag(models.Model):
    title = models.CharField(max_length=55)
    slug = AutoSlugField(populate_from='title', always_update=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = "Теги"
        ordering = ['title']


# class Author(models.Model):
#     nickname = models.CharField(max_length=50)
#     slug = AutoSlugField(populate_from='title')
#
#     def __str__(self):
#         return self.nickname
#
#     def get_absolute_url(self):
#         return reverse('author', kwargs={'slug': self.slug})
#
#     class Meta:
#         verbose_name = 'Автор'
#         verbose_name_plural = "Авторы"
#         ordering = ['nickname']


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', always_update=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = AutoSlugField(populate_from='title', always_update=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', default=User.username)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = "Посты"
        ordering = ['-created_at']


