# Generated by Django 2.2.6 on 2020-03-27 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200327_2205'),
        ('forums', '0004_forum_forum_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumcomment',
            name='forum_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile'),
        ),
    ]
