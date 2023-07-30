# cyber-mooc/mysite/login_attempt_middleware.py

from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.http import HttpResponseForbidden

class LoginAttemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the user's IP address. This is just one way to identify a user for simplicity.
        ip_address = request.META.get('REMOTE_ADDR')

        # Get the user's login attempt count from the cache.
        login_attempts = cache.get(f'login_attempts_{ip_address}', 0)

        # Check if the user has exceeded the maximum number of login attempts.
        if login_attempts >= settings.LOGIN_ATTEMPTS_MAX:
            return HttpResponseForbidden("Too many login attempts. Please try again later.")

        # Process the request and get the response.
        response = self.get_response(request)

        # If the login was unsuccessful (e.g., wrong credentials), increment the login attempts counter.
        if response.status_code == 200 and 'login' in request.path and request.method == 'POST':
            login_attempts += 1
            cache.set(f'login_attempts_{ip_address}', login_attempts, settings.LOGIN_ATTEMPTS_TIMEOUT)

        return response
