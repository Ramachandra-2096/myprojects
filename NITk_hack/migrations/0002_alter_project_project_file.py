# Generated by Django 3.2.6 on 2023-12-28 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nitk_hack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_file',
            field=models.FileField(upload_to='Nitk_hack/uploads'),
        ),
    ]