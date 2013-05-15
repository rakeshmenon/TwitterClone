from .models import Tweet
from .forms import TweetForm
from apps.accounts.models import UserProfile
from django.views.generic.base import View
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger('logview.tweet')


def JSONResponse(response_object):
    '''
    Returns a HTTP Response object with json type response.
    response_object: Dictionary object to jsonify
    '''
    from django.shortcuts import HttpResponse
    return HttpResponse(
                            content=json.dumps(
                                                    response_object,
                                                    indent=3,
                                                    cls=DjangoJSONEncoder
                                              ),
                            content_type='application/json'
                       )


class TweetView(View):
    def get(self, request, *args, **kwargs):
        response = {
                        'status': 'failed',
                        'messages': 'Default error message',
                        'code': -1
                    }
        try:
            # Fetch top results
            if kwargs.get('arg', None) == 'self':
                results = self.get_top_posts(request.user, True)
            else:
                results = self.get_top_posts(request.user)

            # Prepare the response
            response = {
                            'status': 'success',
                            'messages': results,
                            'code': 1
                        }
        except:
            logger.exception('Unknown exception in TweetView GET request!')
            response['messages'] = u'Unknown error occurred!'

        return JSONResponse(response)

    def get_top_posts(self, current_user, only=False):
        # Get follows list
        if not only:
            follows = list(UserProfile.objects.get(user=current_user).follows.all())
            follows.append(current_user)
            results = Tweet.objects.filter(owner__in=follows).order_by('-posted_on').values('content', 'posted_on', 'owner__username')
        else:
            results = Tweet.objects.filter(owner=current_user).order_by('-posted_on').values('content', 'posted_on', 'owner__username')
        # Always return top 20 results
        return list(results)[:20]

    def post(self, request, *args, **kwargs):
        response = {
                        'status': 'failed',
                        'messages': 'Default error message',
                        'code': -1
                    }

        form = TweetForm(request.POST)

        try:
            if form.is_valid():
                form.save(request.user)

                response = {
                                'status': 'success',
                                'messages': form.cleaned_data,
                                'code': 1
                           }

            else:
                response['messages'] = form.errors
                logger.error('Error in Form POST. Errors = {errors}'.format(errors=form.errors))

        except:
            response['messages'] = u"Unknown Exception during TweetView POST request"
            logger.exception('Unknown Exception during TweetView POST request')

        return JSONResponse(response)

        @method_decorator(login_required)
        def dispatch(self, request, *args, **kwargs):
            return super(TweetView, self).dispatch(request, *args, **kwargs)

