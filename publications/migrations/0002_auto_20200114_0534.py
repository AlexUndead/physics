# Generated by Django 3.0.1 on 2020-01-14 02:34

from django.db import migrations

def create_publications_no_category(apps, schema_editor):
    Category = apps.get_model('publications', 'Category')
    no_category = Category(name='Без категории', url='')
    no_category.save()

class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
            migrations.RunPython(create_publications_no_category),
    ]
