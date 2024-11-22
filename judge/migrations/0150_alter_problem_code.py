# Generated by Django 3.2.25 on 2024-11-22 09:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0149_recommendationdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='code',
            field=models.CharField(help_text='A short, unique code for the problem, used in the URL after /problem/', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[a-z0-9]+$', 'Problem code must be ^[a-z0-9]+$')], verbose_name='problem code'),
        ),
    ]
