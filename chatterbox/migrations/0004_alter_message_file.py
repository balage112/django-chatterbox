# Generated by Django 4.1.1 on 2022-09-21 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatterbox', '0003_message_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='file',
            field=models.TextField(blank=True, null=True),
        ),
    ]
