# Generated by Django 4.2.4 on 2023-10-05 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Diet', '0002_giornodieta_cal_giornodieta_carboidrati_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giornodieta',
            name='giorno',
            field=models.IntegerField(auto_created=True, default=1, unique=True),
        ),
    ]