import json

import pymysql


def load_data():
    with open("./cities.json", "r") as file:
        # print(file.read())
        json_file = json.loads(file.read())
        json_file_val = json_file.get("returnValue")
        # print(type(json_file_val)
    return json_file_val

def insert_data(cities):
    db = pymysql.Connect(host="localhost", port=3306, user="root",
                         password="Maverick2019!", database="flask_proj", charset="utf8")
    cursor = db.cursor()
    for key in cities.keys():
        cursor.execute("insert into city_letter_model(letter) values ('%s');" % key)
        db.commit()
        cursor.execute("select city_letter_model.id from city_letter_model where letter='%s';" % key)
        letter_id = cursor.fetchone()[0]
        # print(key)
        # print(letter_id)
        city_list = cities.get(key)
        for city in city_list:
            print(city)

            cursor.execute("insert into cities_model(letter_id, city_id, city_parent_id, city_code, city_name, city_pinyin)"+
                       " values (%d, %d, %d, %d, '%s', '%s');" % (letter_id, city["id"], city["parentId"],
                                                             city["cityCode"], city["regionName"], city["pinYin"]))
            db.commit()


if __name__ == '__main__':
    cities = load_data()
    insert_data(cities)