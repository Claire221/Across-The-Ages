# Generated by Django 3.2.16 on 2023-01-31 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='description',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='title',
        ),
        migrations.AddField(
            model_name='contact',
            name='email',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='first_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]