from django.conf.urls import url
from . import apis

urlpatterns = [
    # post views
    url(r'^register/$', apis.register, name='register'),
]
