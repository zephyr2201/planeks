from . import apis
from django.conf.urls import url

urlpatterns = [
    url(r'^register/$', apis.register, name='register'),
    url(r'^download/(?P<pk>.+)$', apis.download_file, name='download-file'),
    url(r'^generate/(?P<pk>.+)$', apis.process_generate, name='generate-fake-data')
]
