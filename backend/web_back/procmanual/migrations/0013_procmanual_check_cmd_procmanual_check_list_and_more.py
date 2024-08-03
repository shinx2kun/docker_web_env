# Generated by Django 5.0.6 on 2024-07-27 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procmanual', '0012_remove_procmanual_check_cmd'),
    ]

    operations = [
        migrations.AddField(
            model_name='procmanual',
            name='check_cmd',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='procmanual',
            name='check_list',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='procmanual',
            name='execute_cmd',
            field=models.JSONField(default=list),
        ),
    ]
