from django.conf.urls import url
from . import apis

urlpatterns = [
    url(r'^register/$', apis.register, name='register'),
    url(r'^download/(?P<pk>.+)$', apis.download_file, name='download-file'),
]
