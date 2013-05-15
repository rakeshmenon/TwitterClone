from django.conf.urls import patterns, include, url
from apps.accounts.views import Login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', Login.as_view( template_name='index.html' ), name='home'),
    url(r'^user/', include('apps.accounts.urls')),
    url(r'^tweet/', include('apps.tweet.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
