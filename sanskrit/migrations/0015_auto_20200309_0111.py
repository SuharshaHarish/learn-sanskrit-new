# Generated by Django 2.2.6 on 2020-03-08 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanskrit', '0014_sanskritlessons_lessons_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanskritquestions',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]