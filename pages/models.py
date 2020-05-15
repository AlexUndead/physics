from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Page(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, db_index=True, verbose_name="Активность")
    url = models.SlugField(unique=True, verbose_name="ЧПУ")
    title = models.CharField(max_length=100, verbose_name="Название страницы")
    description = RichTextUploadingField()

    def __str__(self):
        return self.title
