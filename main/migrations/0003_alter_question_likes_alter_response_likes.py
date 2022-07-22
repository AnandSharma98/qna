# Generated by Django 4.0.5 on 2022-07-20 13:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_remove_question_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='likes',
            field=models.ManyToManyField(related_name='question_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='response',
            name='likes',
            field=models.ManyToManyField(related_name='response_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]