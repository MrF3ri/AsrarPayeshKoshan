from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('لطفا ابتدا وارد شوید.', 'warning')
            return redirect(url_for('admin.login'))
        if not current_user.is_active:
            flash('حساب کاربری شما غیرفعال است.', 'danger')
            return redirect(url_for('admin.logout'))
        return f(*args, **kwargs)
    return decorated_function