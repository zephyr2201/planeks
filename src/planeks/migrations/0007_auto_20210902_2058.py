# Generated by Django 3.1.6 on 2021-09-02 14:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('planeks', '0006_auto_20210902_2025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='csv',
            options={'verbose_name': 'New schema', 'verbose_name_plural': 'New schema'},
        ),
        migrations.AddField(
            model_name='csv',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='csv',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.DeleteModel(
            name='Column',
        ),
    ]
