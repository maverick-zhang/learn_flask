"""
insert into movies(id, showname, shownameen, director, leadingRole, type, country, language, duration,
screeningmodel, openday, backgroundpicture, flag, isdelete) values(228830,"梭哈人生","The Drifting Red Balloon",
"郑来志","谭佑铭,施予斐,赵韩樱子,孟智超,李林轩","剧情,爱情,喜剧","中国大陆","汉语普通话",90,"4D",date("2018-01-30 00:00:00"),
"i1/TB19_XCoLDH8KJjy1XcXXcpdXXa_.jpg",1,0);

"""


from App.extensions import models
from App.models import BaseModel


class MovieModel(BaseModel):
    showName = models.Column(models.String(64))
    showNameEn = models.Column(models.String(128))
    director = models.Column(models.String(64))
    leadingRole = models.Column(models.String(256))
    movieType = models.Column(models.String(64))
    country = models.Column(models.String(64))
    language = models.Column(models.String(64))
    duration = models.Column(models.Integer, default=90)
    screeningModel = models.Column(models.String(32))
    openDay = models.Column(models.DateTime)
    bgPicture = models.Column(models.String(256))
    flag = models.Column(models.Boolean, default=False)
    is_delete = models.Column(models.Boolean, default=False)



