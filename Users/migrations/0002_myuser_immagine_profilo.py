# Generated by Django 4.2.4 on 2023-10-14 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='immagine_profilo',
            field=models.ImageField(blank=True, upload_to='fotouser/'),
        ),
    ]
