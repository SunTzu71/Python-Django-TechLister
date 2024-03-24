
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class RecruiterAccessMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # check if path requires to be authenticated
        if request.path.startswith('/recruiter/'):
            if not request.user.is_authenticated or not request.session.get('recruiter'):
                return redirect('/')

        response = self.get_response(request)
        return response
