# Generated by Django 5.0.5 on 2024-05-16 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0007_commentpost_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.IntegerField(default=0),
        ),
    ]
