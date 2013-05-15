from django.conf.urls.defaults import patterns, url
from .views import Register, Login, ProfileView

urlpatterns = patterns('apps.accounts.views',
    url(
            r'^register$', Register.as_view(), name='register'
        ),
    url(
            r'^login$',
            Login.as_view(
                            template_name='index.html',
                            addnl_context_data={'test': 'This is test val'}
                         ),
            name='login'
        ),
    url(
            r'^logout$', 'userlogout', name='logout'
        ),
    url(
            r'^profile$', ProfileView.as_view(), name='user-profile'
        ),
)
