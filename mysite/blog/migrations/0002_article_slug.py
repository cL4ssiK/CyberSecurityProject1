# Generated by Django 4.2.5 on 2024-03-11 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(default='empty'),
            preserve_default=False,
        ),
    ]
