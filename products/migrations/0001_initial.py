# Generated by Django 3.2.24 on 2024-02-22 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('display_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='PastryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('display_name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('batch_size', models.IntegerField()),
                ('ingredients', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('image_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('prop_type', models.JSONField(blank=True, null=True)),
                ('prop_contents', models.JSONField(blank=True, null=True)),
                ('prop_icing', models.JSONField(blank=True, null=True)),
                ('prop_toppings', models.JSONField(blank=True, null=True)),
                ('prop_text', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grouped_products', to='products.category')),
            ],
        ),
    ]
