from flask_admin.contrib.sqla import ModelView

from flask_login import current_user
from werkzeug.exceptions import (
    Unauthorized,
    Forbidden,
)


class ProtectedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            raise Unauthorized
        if not current_user.is_admin:
            raise Forbidden
