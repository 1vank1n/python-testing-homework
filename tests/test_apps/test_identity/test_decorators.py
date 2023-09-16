from http import HTTPStatus

import pytest
from django.conf import LazySettings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory
from django.views import View

from server.apps.identity.intrastructure.django.decorators import redirect_logged_in_users
from server.common.django.decorators import dispatch_decorator
from django.contrib.auth.decorators import user_passes_test


# def test_redirect_logged_in_users(rf: RequestFactory, settings: LazySettings, ) -> None:
#     request = rf.get('/')
#     request.user = AnonymousUser()

#     @dispatch_decorator(redirect_logged_in_users())
#     class TestView(View):
#         def get(self, *args, **kwargs):
#             return HttpResponse()

#     response = TestView.as_view()(request)
#     assert response.status_code  ==  HTTPStatus.OK


# def test_redirect_logged_in_users() -> None:
#     assert redirect_logged_in_users() == user_passes_test
