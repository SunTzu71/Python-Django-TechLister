# Generated by Django 5.0.3 on 2024-03-18 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_portfolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='end_year',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
