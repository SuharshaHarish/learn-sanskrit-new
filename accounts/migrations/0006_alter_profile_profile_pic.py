# Generated by Django 3.2.4 on 2021-06-16 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200327_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='pics/Default-Profile-Pic.png', upload_to='pics/'),
        ),
    ]