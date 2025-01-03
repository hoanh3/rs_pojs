# Generated by Django 3.2.25 on 2024-11-22 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0151_alter_navigationbar_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemgroup',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='problem group ID'),
        ),
        migrations.AlterField(
            model_name='problemtype',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='problem category ID'),
        ),
    ]
