from django.utils import timezone
from django.db import models
from django.db.models.deletion import CASCADE


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Csv(BaseModel):
    SEPARATORS = [('1', 'Comma(,)'), ('2', 'Semicolon(;)')]
    QUOTE = [('1', 'Double-quote(")'), ('2', "Single-quote(')")]
    row = models.IntegerField(null=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    column_separator = models.CharField(max_length=50, null=False, choices=SEPARATORS)
    string_characters = models.CharField(max_length=50, null=False, choices=QUOTE)
    csv_file = models.FileField(upload_to='media', blank=True, null=True)

    class Meta:
        verbose_name = 'New schema'
        verbose_name_plural = 'New schema'


class Column(models.Model):
    CHOICES = [
        ('1', 'Full name'), ('2', 'Job'),
        ('3', 'Email'), ('4', 'Site'),
        ('5', 'Phone number'), ('6', 'Company'),
        ('7', 'Text'), ('8', 'Integer'),
        ('9', 'Address'), ('10', 'Date'),
    ]
    column_name = models.CharField(max_length=50, blank=False, null=False)
    type = models.CharField(max_length=50, null=False, choices=CHOICES)
    order = models.IntegerField()
    csv = models.ForeignKey(Csv, on_delete=CASCADE, null=True, related_name='columns')
