from .forms import SignupForm, LoginForm, UserDetailsForm
from .models import UserProfile
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.views.generic.base import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token

import logging
logger = logging.getLogger('logview.accounts')


class Register(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwarg):
        result = {
                    'status': 'failed', # 'success', 'failed'
                    'messages': 'This API accepts POST requests only!',
                    'code': -1       # -1 is default. All valid codes must be > 0
                 }

        form = SignupForm(request.POST)

        try:
            if form.is_valid():
                user = form.authenticate(request)

                if user:
                    result['status']  = 'success'
                    result['code']    = 1
                    result['messages'] = u'Registration Successful. User is now logged in!'
                else:
                    result['messages'] = u'User not authenticated!'
            else:
                result['messages'] = form.errors
        except:
            result['messages'] = u'Unknown Error/Exception!'
            logger.exception('Exception encountered during registration!')

        return JSONResponse(result)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Register, self).dispatch(request, *args, **kwargs)


class Login(TemplateView):
    addnl_context_data = {}

    def post(self, request, *args, **kwarg):
        result = {
                    'status': 'failed', # 'success', 'failed'
                    'messages': '',
                    'code': -1       # -1 is default. All valid codes must be > 0
                 }
        form = LoginForm(request.POST)
        try:
            if form.is_valid():
                user = form.authenticate(request)
                if user:
                    result['status']  = 'success'
                    result['code']    = 1
                    result['messages'] = u'Login Successful!'
                else:
                    result['messages'] = u'User not authenticated!'
            else:
                result['messages'] = form.errors
        except:
            result['messages'] = u'Unknown Error/Exception!'
            logger.exception('Exception encountered during registration!')

        return JSONResponse(result)

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)

        # Update context with more data for template
        # context['more_data'] = more_data
        context.update(self.addnl_context_data)
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        return super(Login, self).dispatch(request, *args, **kwargs)

class ProfileView(View):
    def post(self, request, *args, **kwargs):
        result = {
                    'status': 'failed', # 'success', 'failed'
                    'messages': '',
                    'code': -1       # -1 is default. All valid codes must be > 0
                 }

        form = UserDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                profile = UserProfile.get(user=request.user)
                profile.image = form.cleaned_data['image']
                profile.save()

                form.save(profile)

                result['status']  = 'success'
                result['code']    = 1
                result['messages'] = u'Profile Update Successful!'

            except:
                result['messages'] = u'Profile Update Failed!'
                logger.exception('Exception during Userprofile Update!')
        else:
            logger.error('Form error: Message = %s' % form.errors)
            result['messages'] = form.errors

        return JSONResponse(result)

    def get(self, request, *args, **kwargs):
        response =  {
                        'status': 'failed',
                        'messages': '',
                        'code': -1
                    }

        try:
            profile = UserProfile.objects.get(user=request.user)

            result = profile.get_user_details()

            response =  {
                            'status': 'success',
                            'messages': result,
                            'code': 1
                        }
        except:
            response['messages'] = u'Unknown except in Profile GET request'
            logger.exception('Exception encountered in Profile GET request')

        return JSONResponse(response)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)


def userlogout(request):
    '''
    Performs a logout operation to the currently logged in user.
    request: Middleware request object, that stores current user request
    '''
    try:
        logout(request)
    except:
        logger.exception('Exception during logout')

    return HttpResponseRedirect(reverse('home'))


def JSONResponse(response_object):
    '''
    Returns a HTTP Response object with json type response.
    response_object: Dictionary object to jsonify
    '''
    return HttpResponse(
                            content=json.dumps(
                                                    response_object,
                                                    indent=3,
                                                    cls=DjangoJSONEncoder
                                              ),
                            content_type='application/json'
                       )
