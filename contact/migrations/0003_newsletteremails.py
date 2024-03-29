# Generated by Django 3.2.24 on 2024-03-26 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20240322_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterEmails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=320, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('received_codes', models.TextField(blank=True, null=True)),
                ('used_codes', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
