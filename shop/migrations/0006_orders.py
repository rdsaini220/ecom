# Generated by Django 3.0.2 on 2020-02-20 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200204_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('items_json', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=90)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=500)),
                ('address2', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('phone_no', models.IntegerField(default='0')),
                ('zip_code', models.IntegerField(default='0')),
            ],
        ),
    ]
