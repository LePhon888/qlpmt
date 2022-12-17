from functools import wraps
from flask_login import current_user
from flask import redirect, url_for


def annonymous_user(f):
    @wraps(f)
    def decorated_func(*args, **kwrags):
        if current_user.is_authenticated:
            return redirect('/')
        return f(*args, **kwrags)

    return decorated_func


def requires_access_level(current_user):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.user_role.name == 'CASHIER':
                return redirect('payment_bill')
            elif current_user.user_role.name == 'NURSE':
                return redirect('medical_list')
            elif current_user.user_role.name == 'DOCTOR':
                return redirect('medical-report')
            return f(*args, **kwargs)

        return decorated_function

    return decorator
