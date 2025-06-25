from functools import wraps
from django.http import HttpResponseForbidden

def user_in_group(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this resource.")
        return _wrapped_view
    return decorator