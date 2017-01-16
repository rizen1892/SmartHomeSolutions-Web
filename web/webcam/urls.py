from django.conf.urls import *
from django.contrib import admin
from django.conf import settings
from home import views as myapp

admin.autodiscover()

urlpatterns = [
    url(r'^$', myapp.home, name='home'),
    url(r'^' + settings.PREFIX + r'$', myapp.home, name='home'),
    url(r'^' + settings.PREFIX + r'about$', myapp.about, name='about'),
    url(r'^' + settings.PREFIX + r'movements$', myapp.movements, name='movements'),
    url(r'^' + settings.PREFIX + r'movements/(?P<page>[\d]+)$', myapp.movements, name='movements'),
    url(r'^' + settings.PREFIX + r'details/(?P<movement_id>[\d]+)$', myapp.movement_details, name='movement_details'),
    url(r'^' + settings.PREFIX + r'stream$', myapp.stream, name='stream'),
    url(r'^' + settings.PREFIX + r'stream_data$', myapp.stream_data, name='stream_data'),
    url(r'^' + settings.PREFIX + r'configuration$', myapp.configuration, name='configuration'),
    url(r'^' + settings.PREFIX + r'configuration/restart_app$', myapp.restart_app, name='restart_app'),
    url(r'^' + settings.PREFIX + r'configuration/restart_pi$', myapp.restart_pi, name='restart_pi'),
    url(r'^' + settings.PREFIX + r'configuration/shutdown_pi$', myapp.shutdown_pi, name='shutdown_pi'),
    url(r'^' + settings.PREFIX + r'admin/', include(admin.site.urls)),
]
