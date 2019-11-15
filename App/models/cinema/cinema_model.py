from App.extensions import models
from App.models import BaseModel

"""
insert into cinemas(name,city,district,address,phone,score,hallnum,servicecharge,astrict,flag,isdelete)
 values("深圳戏院影城","深圳","罗湖","罗湖区新园路1号东门步行街西口","0755-82175808",9.7,9,1.2,20,1,0);

"""


# class CinemaAddress(BaseModel):
#     c_user_id = db.Column(db.Integer, db.ForeignKey(CinemaUser.id))
#     name = db.Column(db.String(64))
#     city = db.Column(db.String(16))
#     district = db.Column(db.String(16))
#     address = db.Column(db.String(128))
#     phone = db.Column(db.String(32))
#     score = db.Column(db.Float, default=10)
#     hallnum = db.Column(db.Integer, default=1)
#     servicecharge = db.Column(db.Float, default=10)
#     astrict = db.Column(db.Float, default=10)
#     flag = db.Column(db.Boolean, default=False)
#     is_delete = db.Column(db.Boolean, default=False)

class CinemaModel(BaseModel):
    name = models.Column(models.String(64))
    city = models.Column(models.String(16))
    district = models.Column(models.String(16))
    address = models.Column(models.String(128))
    phone = models.Column(models.String(16))
    score = models.Column(models.Float, default=10)
    hallNum = models.Column(models.Integer, default=1)
    serviceCharge = models.Column(models.Float, default=10)
    aStrict = models.Column(models.Float, default=10)
    flag = models.Column(models.Boolean, default=False)
    is_delete = models.Column(models.Boolean, default=False)
    is_verified = models.Column(models.Boolean, default=False)
