from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import available_attrs, method_decorator


def require_own_agency(view_function):
    @method_decorator(login_required)
    @wraps(view_function, assigned=available_attrs(view_function))
    def _wrapped_view(self, *args, **kwargs):
        object_org = self.get_object_agency()

        # Test function
        def _test_function(user):
            if not user.is_staff:
                return object_org == user
            return True

        # This is the function that we're returning. It's wrapped with user_passes_test
        @user_passes_test(_test_function)
        def _continue_function(request, *args2, **kwargs2):
            return view_function(self, *args2, **kwargs2)

        return _continue_function(self.request, *args, **kwargs)

    return _wrapped_view