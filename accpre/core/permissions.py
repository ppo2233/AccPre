import re

from rest_framework.permissions import IsAuthenticated

from accpre import settings


class AccPreIsAuthenticated(IsAuthenticated):
    """ AccPre的用户认证校验 """

    def has_permission(self, request, view):
        for release in settings.CERTIFICATION_PASS_LIST:
            request_url = str(request._request.path)
            if release in request_url:
                return True
        return bool(request.user and request.user.is_authenticated)
