# Generated by Django 3.0.3 on 2020-03-09 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='custom_category_provided',
        ),
        migrations.RemoveField(
            model_name='account',
            name='custom_source_provided',
        ),
        migrations.AlterField(
            model_name='account',
            name='custom_source',
            field=models.CharField(max_length=100000),
        ),
    ]
