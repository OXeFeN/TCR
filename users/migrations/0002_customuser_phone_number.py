# Generated by Django 5.1.5 on 2025-04-04 09:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default='nevyplneno', max_length=20, validators=[django.core.validators.RegexValidator('^\\+?[\\d\\s]+$', 'Zadejte platné telefonní číslo.')], verbose_name='Telefonní číslo'),
            preserve_default=False,
        ),
    ]
