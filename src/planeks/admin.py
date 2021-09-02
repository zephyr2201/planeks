from django.contrib import admin
from .models import Csv
from .forms import ColumnTabularInline


@admin.register(Csv)
class CsvAdmin(admin.ModelAdmin):
    inlines = [ColumnTabularInline]
    list_display = ('name', 'updated_at')

    def get_fields(self, request, obj):
        return ['name', 'column_separator']
