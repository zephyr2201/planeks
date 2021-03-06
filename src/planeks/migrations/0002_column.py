# Generated by Django 3.1.6 on 2021-09-02 10:06

from typing import Callable
from django.db import migrations, models
from django.db.models.deletion import CASCADE


class Migration(migrations.Migration):

    dependencies = [
        ('planeks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=30)),
                ('type', models.CharField(choices=[('1', 'First'), ('2', 'Second')], max_length=30)),
                ('order', models.IntegerField()),
                ('csv', models.ForeignKey(related_name='columns', on_delete=CASCADE, to='planeks.Csv')),
            ],
        ),
    ]
