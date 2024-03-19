# Generated by Django 3.2.24 on 2024-03-15 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20240227_0940'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='favorite_breads',
            field=models.ManyToManyField(to='products.BreadProduct'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='favorite_pastries',
            field=models.ManyToManyField(to='products.PastryProduct'),
        ),
    ]