# Generated by Django 5.0.3 on 2024-03-12 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='currently_working',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='order',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='start_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='task_one',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
