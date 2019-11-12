from werkzeug.security import generate_password_hash, check_password_hash

from App.extensions import models
from App.models import BaseModel
from App.models.movie_user.model_constants import PERMISSIONS_NONE


class CustomerModel(BaseModel):
    name = models.Column(models.String(64))
    _password = models.Column(models.String(256), nullable=False)
    phone = models.Column(models.String(32), unique=True)
    is_delete = models.Column(models.Boolean, default=False)
    permission = models.Column(models.Integer, default=PERMISSIONS_NONE)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd_val):
        self._password = generate_password_hash(pwd_val)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)
