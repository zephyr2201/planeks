from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Csv
from .forms import ColumnTabularInline


@admin.register(Csv)
class CsvAdmin(admin.ModelAdmin):
    inlines = [ColumnTabularInline]
    list_display = ('name', 'updated_at', 'status', 'account_actions', 'download_link')

    def get_fields(self, request, obj):
        return ['name', 'column_separator', 'string_characters', 'row', ]

    def download_link(self, obj):
        if obj.csv_file:
            return format_html(
                '<a href="{}">Download</a>',
                reverse('download-file', args=[obj.pk])
            )
    download_link.short_description = "Download"

    # Link to generate csv file
    def account_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Generate data</a>',
            reverse('generate-fake-data', args=[obj.pk]),
        )
    account_actions.short_description = 'Action'

    def status(self, obj):
        if obj.csv_file:
            return format_html("<p style='color:green'><b>Ready</b></p>")
        else:
            return format_html("<p style='color:orange'><b>Processing</b></p>")
