# Generated by Django 3.2.7 on 2021-10-27 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='threadmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
