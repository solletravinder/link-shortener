# Generated by Django 2.2.2 on 2019-06-29 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortUrl', models.CharField(blank=True, max_length=255, null=True)),
                ('longUrl', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
