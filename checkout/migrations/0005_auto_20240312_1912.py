# Generated by Django 3.2.24 on 2024-03-12 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_auto_20240310_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_city',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_county',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_line1',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_line2',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_postcode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
