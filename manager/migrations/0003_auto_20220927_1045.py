# Generated by Django 2.2.27 on 2022-09-27 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_permissionlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountuser',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='permissionlog',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
