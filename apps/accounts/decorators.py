# File: apps/accounts/decorators.py

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            # ইউজারের রোল যদি অ্যালাউড রোলের মধ্যে থাকে, তবেই অ্যাক্সেস পাবে
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            # অন্যথায় পারমিশন ডিনাইড (403 Forbidden) দেখাবে
            raise PermissionDenied
        return _wrapped_view
    return decorator