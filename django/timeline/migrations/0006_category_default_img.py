# Generated by Django 3.2.7 on 2021-10-18 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0005_auto_20211017_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='default_img',
            field=models.ImageField(default='images/default.jpeg', upload_to='images/', verbose_name='デフォルト画像'),
        ),
    ]
