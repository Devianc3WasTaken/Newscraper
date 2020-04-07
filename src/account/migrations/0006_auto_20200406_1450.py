# Generated by Django 3.0.3 on 2020-04-06 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_account_source1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='source1',
            new_name='bbcSource',
        ),
        migrations.AddField(
            model_name='account',
            name='categoryCoronaVirus',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='account',
            name='categoryPolitics',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='account',
            name='categorySport',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='guardianSource',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='account',
            name='independentSource',
            field=models.BooleanField(default=False),
        ),
    ]
