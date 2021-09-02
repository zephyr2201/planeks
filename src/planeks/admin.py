from django.contrib import admin
from django.urls import reverse
from django.conf.urls import url
from django.utils.html import format_html
from django.http.response import HttpResponseRedirect

from .models import Csv
from .services import (
    writer_csv,
    generate_fake_data,
)
from .selectors import fetch_csv
from .forms import ColumnTabularInline


@admin.register(Csv)
class CsvAdmin(admin.ModelAdmin):
    inlines = [ColumnTabularInline]
    list_display = ('name', 'updated_at', 'account_actions')

    def get_fields(self, request, obj):
        return ['name', 'column_separator', 'string_characters', 'row']

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            url(r'^(?P<pk>.+)$', self.process_generate, name='generate-fake-data',),
        ]
        return urls

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
        row = csv_obj.row
        for column in csv_obj.columns.all().order_by('order'):
            header.append(column.column_name)
            types.append(column.type)
        data = generate_fake_data(types, row)
        writer_csv(csv_obj, data, header)
        return HttpResponseRedirect('.')
