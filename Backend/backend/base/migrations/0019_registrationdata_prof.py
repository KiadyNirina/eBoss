# Generated by Django 5.0.3 on 2024-08-23 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_registrationdata_classes_registrationdata_prof_de_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationdata',
            name='prof',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
