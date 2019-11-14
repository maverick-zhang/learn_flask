from werkzeug.security import generate_password_hash, check_password_hash

from App.extensions import models
from App.models import BaseModel
from App.models.model_constants import COMMON_CUSTOMER


class CustomerModel(BaseModel):
    name = models.Column(models.String(64))
    _password = models.Column(models.String(256), nullable=False)
    phone = models.Column(models.String(32), unique=True)
    is_delete = models.Column(models.Boolean, default=False)
    permission = models.Column(models.Integer, default=COMMON_CUSTOMER)

    @property
    def password(self):
        raise AttributeError("THE PASSWORD IS NOT ACCESSIBLE")

    @password.setter
    def password(self, pwd_val):
        self._password = generate_password_hash(pwd_val)

    def check_password(self, pwd):
        return check_password_hash(self._password, pwd)
