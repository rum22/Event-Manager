# Generated by Django 3.0.4 on 2020-04-22 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_remove_post_bookmarks'),
        ('organizations', '0003_auto_20200421_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile_org',
            name='bookmarks',
            field=models.ManyToManyField(to='event.Post'),
        ),
    ]
