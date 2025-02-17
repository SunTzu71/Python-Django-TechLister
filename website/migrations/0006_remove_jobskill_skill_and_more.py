# Generated by Django 5.0.3 on 2024-05-02 13:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_aitoken'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobskill',
            name='skill',
        ),
        migrations.AlterUniqueTogether(
            name='userskill',
            unique_together={('user', 'skill_name')},
        ),
        migrations.RemoveField(
            model_name='userskill',
            name='skill',
        ),
    ]
