from django.db import models

class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, db_index=True, verbose_name="Активность")
    name = models.CharField(max_length=100, verbose_name="Название категории")
    url = models.SlugField(unique=True, verbose_name="ЧПУ")

    def __str__(self):
        return self.name

class Page(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, db_index=True, verbose_name="Активность")
    url = models.SlugField(unique=True, verbose_name="ЧПУ")
    title = models.CharField(max_length=100, verbose_name="Название страницы")
    description = models.TextField(verbose_name="Текст страницы")
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return self.title
