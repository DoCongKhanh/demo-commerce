# Generated by Django 4.1.3 on 2022-11-07 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_category',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, null=True),
        ),
    ]
