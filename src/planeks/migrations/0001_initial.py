# Generated by Django 3.1.6 on 2021-09-02 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Csv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('column_separator', models.CharField(choices=[('1', 'First'), ('2', 'Second')], max_length=10)),
            ],
        ),
    ]
