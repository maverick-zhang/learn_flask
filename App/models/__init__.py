from App.extensions import models


class BaseModel(models.Model):
    __abstract__ = True

    id = models.Column(models.Integer, primary_key=True, autoincrement=True)


    def save(self):
        try:
            models.session.add(self)
            models.session.commit()
        except Exception as e:
            raise
        return True

    def delete(self):

        try:
            models.session.delete(self)
            models.session.commit()
        except Exception as e:
            return False
        return True
