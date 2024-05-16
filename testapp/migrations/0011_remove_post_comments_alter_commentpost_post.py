# Generated by Django 5.0.5 on 2024-05-16 18:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0010_alter_commentpost_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
        migrations.AlterField(
            model_name='commentpost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='testapp.post'),
        ),
    ]
