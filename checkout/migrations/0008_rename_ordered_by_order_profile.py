# Generated by Django 3.2.24 on 2024-03-25 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0007_order_ordered_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ordered_by',
            new_name='profile',
        ),
    ]