from flask_restful import Resource, fields, marshal

from App.api.api_constants import HTTP_OK
from App.models.common.cities import CitiesModel, CityLetterModel

city_fields = {
    "id": fields.Integer(attribute="city_id"),
    "parentId": fields.Integer(attribute="city_patent_id"),
    "cityCode": fields.Integer(attribute="city_code"),
    "regionName": fields.String(attribute="city_name"),
    "pinYin": fields.String(attribute="city_pinyin")
}

class CitiesResource(Resource):
    def get(self):
        letters = CityLetterModel.query.all()
        cities = {}
        letters_cities_fields = {}
        for letter in letters:
            print(letter.id)
            cities_list = CitiesModel.query.filter_by(letter_id=letter.id).all()
            cities[letter.letter] = cities_list
            letters_cities_fields[letter.letter] = fields.List(fields.Nested(city_fields))

        data =  {
            "status": HTTP_OK,
            "msg":"ok",
            "data":marshal(cities, letters_cities_fields)
        }

        return data