# Generated by Django 5.0.3 on 2024-08-09 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_customuser_teacher_subjects_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='activities',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='students_missing',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
