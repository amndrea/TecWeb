# Generated by Django 4.2.4 on 2023-10-15 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_myuser_immagine_profilo'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='obiettivo',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
