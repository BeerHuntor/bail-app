# Generated by Django 5.0.5 on 2024-05-06 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinformation',
            name='display_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]