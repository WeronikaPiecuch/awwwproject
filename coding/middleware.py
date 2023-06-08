from .sdcc_options import *


# Middleware to set default values for session keys
class SessionDefaultMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Set default values for session keys
        for key, value in SESSION_DEFAULTS.items():
            if key not in request.session:
                request.session[key] = value
        
        response = self.get_response(request)
        return response