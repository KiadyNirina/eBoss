# Generated by Django 5.0.3 on 2024-08-20 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_note_school_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='school_year',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='note',
            name='semester',
            field=models.CharField(max_length=50),
        ),
    ]