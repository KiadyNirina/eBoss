# Generated by Django 5.0.3 on 2024-08-22 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_rename_address_customuser_school_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='student_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/students/'),
        ),
    ]