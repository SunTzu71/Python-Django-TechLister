
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class UserAccessMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # check if path requires to be authenticated
        if request.path.startswith('/user/'):
            if not request.user.is_authenticated:
                return redirect('/')

        response = self.get_response(request)
        return response
