# Generated by Django 5.1.4 on 2025-01-11 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movie_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
    ]
