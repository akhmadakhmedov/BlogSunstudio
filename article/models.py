from django.db import models
from ckeditor.fields import RichTextField


class Article(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=50, verbose_name='Названия')
    content = RichTextField(verbose_name='Содержание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    article_photo = models.FileField(blank = True, null = True, verbose_name="Добавить приложение")
    category     = models.CharField(max_length=50, verbose_name='Категория')
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE, verbose_name='Моя статья', related_name='comments')
    comment_author = models.CharField(max_length=50, verbose_name='Имя')
    comment_content = models.CharField(max_length=200, verbose_name='Комментарий')
    comment_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.comment_content
    class Meta:
        ordering = ['-comment_date']
