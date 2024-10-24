# Generated by Django 5.0.3 on 2024-08-20 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_note_school_year_alter_note_semester'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='address',
            new_name='school_address',
        ),
        migrations.AddField(
            model_name='customuser',
            name='student_address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='teacher_address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='student_register_number',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
