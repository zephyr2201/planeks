# Generated by Django 3.1.6 on 2021-09-02 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planeks', '0011_csv_row'),
    ]

    operations = [
        migrations.AddField(
            model_name='csv',
            name='csv_file',
            field=models.FileField(blank=True, null=True, upload_to='media'),
        ),
    ]
