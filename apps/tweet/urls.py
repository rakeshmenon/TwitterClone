from django.conf.urls.defaults import patterns, url
from .views import TweetView

urlpatterns = patterns('apps.accounts.views',
    url(
            r'^(?P<arg>\w+)$', TweetView.as_view(), name='tweet'
        )
)
