from django.contrib import admin
from django.urls import reverse
from django.conf.urls import url
from django.utils.html import format_html
from django.http.response import HttpResponseRedirect

from .models import Csv
from .services import (
    writer_csv,
)
from .selectors import fetch_csv
from .forms import ColumnTabularInline


@admin.register(Csv)
class CsvAdmin(admin.ModelAdmin):
    inlines = [ColumnTabularInline]
    list_display = ('name', 'updated_at', 'status', 'account_actions', 'download_link')

    def get_fields(self, request, obj):
        return ['name', 'column_separator', 'string_characters', 'row', ]

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            url(r'^(?P<pk>.+)$', self.process_generate, name='generate-fake-data',),
        ]
        return urls

    def download_link(self, obj):
        if obj.csv_file:
            return format_html(
                '<a href="{}">Download</a>',
                reverse('download-file', args=[obj.pk])
            )
    download_link.short_description = "Download"

    def account_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Generate data</a>',
            reverse('admin:generate-fake-data', args=[obj.pk]),
        )
    account_actions.short_description = 'Action'

    def process_generate(self, request, pk):
        header = []
        types = []
        csv_obj = fetch_csv(pk)
        for column in csv_obj.columns.all().order_by('order'):
            header.append(column.column_name)
            types.append(column.type)
        writer_csv(csv_obj, types, header)
        return HttpResponseRedirect('.')

    def status(self, obj):
        if obj.csv_file:
            return format_html("<p style='color:green'><b>Ready</b></p>")
        else:
            return format_html("<p style='color:orange'><b>Processing</b></p>")
