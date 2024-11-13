# Generated by Django 5.1.1 on 2024-10-16 08:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_app', '0002_category_alter_product_id_alter_product_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=255)),
                ('min_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('max_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sort_by', models.CharField(default='name', max_length=255)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='search_app.category')),
            ],
        ),
    ]