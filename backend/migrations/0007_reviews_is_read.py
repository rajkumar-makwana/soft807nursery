# Generated by Django 4.1 on 2024-03-06 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_reviews_product_alter_reviews_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='is_read',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
