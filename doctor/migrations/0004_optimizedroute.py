# Generated by Django 4.1.7 on 2023-06-06 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_doctor_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='optimizedRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('appointment1', models.CharField(max_length=255)),
                ('appointment2', models.CharField(max_length=255)),
                ('appointment3', models.CharField(max_length=255)),
                ('appointment4', models.CharField(max_length=255)),
            ],
        ),
    ]