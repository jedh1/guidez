# Generated by Django 3.0.4 on 2020-04-04 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelm', '0007_search_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='recurrence',
            field=models.IntegerField(default=0, max_length=2),
        ),
    ]