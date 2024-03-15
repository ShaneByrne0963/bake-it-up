# Generated by Django 3.2.24 on 2024-03-15 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20240315_1837'),
        ('products', '0005_auto_20240227_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='breadproduct',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorite_breads', to='profiles.UserProfile'),
        ),
        migrations.AddField(
            model_name='pastryproduct',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorite_pastries', to='profiles.UserProfile'),
        ),
    ]
