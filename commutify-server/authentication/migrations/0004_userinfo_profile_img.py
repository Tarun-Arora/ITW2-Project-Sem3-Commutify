# Generated by Django 3.2.6 on 2021-11-08 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='profile_img',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]