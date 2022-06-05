import pymongo
from flask import Flask, request, jsonify, make_response
from configparser import ConfigParser
import pandas as pd
from bson.objectid import ObjectId
import json
import datetime
from flask_cors import CORS
import bson.json_util as json_util

app = Flask(__name__)
CORS(app)
config = ConfigParser()
config.read('app.cfg')
host = config['HOST']['host']
port = config['HOST']['port']
username = config['CREDENTIALS']['username']
password = config['CREDENTIALS']['password']

client = pymongo.MongoClient("mongodb+srv://"+username+":"+password+"@cluster0.fnvrd.mongodb.net/?retryWrites=true&w=majority")
mydb = client["Airbnb"]
house_collection = mydb["Home"]
reservation_collection = mydb["Reservation"]


@app.route('/getHousesByDate')
def getDateHouses():
    input_json = request.get_json()
    start_date_input = input_json['start_date']
    end_date_input = input_json['end_date']
    start_date = datetime.datetime(start_date_input['year'], start_date_input['month'], start_date_input['day'])
    end_date = datetime.datetime(end_date_input['year'], end_date_input['month'], end_date_input['day'])
    houses = house_collection.find()
    houses_id_list = []
    houses_list = []
    reservation_list = []

    for i in houses:
        new_dict = {"_id": i['_id'], "sahipID": i['sahipID'], "price": i['price'], "adres": i['adres'], "sehir": i['sehir'], "long": i['long'], "lat": i['lat'], "image_url": i['image_url'],
                    "desc": i['desc'], "title": i['title']}
        houses_list.append(new_dict)

    for a in houses_list:
        houses_id_list.append(a['_id'])

    reservations = reservation_collection.find()
    for i in reservations:
        new_dict1 = {"_id": i['_id'], "start-date": i['start-date'], "end-date": i['end-date'], "home_id": i['home_id'], "user_id": i['user_id']}
        reservation_list.append(new_dict1)

    for id in houses_id_list:
        for res in reservation_list:
            print(type(id))
            print(type(res['home_id']))
            if (id == ObjectId(res['home_id'])) & ( ((start_date >= res['start-date']) & (end_date <= res['end-date'])) | ((start_date <= res['start-date']) & (end_date >= res['end-date'])) ):
                houses_id_list.remove(id)

    selected_houses = house_collection.find({"_id": {"$in": houses_id_list}})

    house_list_new = []
    for i in selected_houses:
        house_list_new.append(i)

    output_json = json_util.dumps(house_list_new)
    return output_json


@app.route('/getHousesByDesc', methods=['POST'])
def getHousesByDesc():
    input_json = request.get_json()
    keyword = input_json['keyword']
    myquery = {"desc": keyword}
    houses = house_collection.find(myquery)
    houses_list = []
    for i in houses:
        new_dict = {"_id": i['_id'], "sahipID": i['sahipID'], "price": i['price'], "adres": i['adres'], "sehir": i['sehir'], "long": i['long'], "lat": i['lat'], "image_url": i['image_url'],
                    "desc": i['desc'], "title": i['title']}
        houses_list.append(new_dict)
    output_json = json_util.dumps(houses_list)
    return output_json


@app.route('/getHousesByTitle')
def getHousesByTitle():
    input_json = request.get_json()
    keyword = input_json['keyword']
    myquery = {"title": keyword}
    houses = house_collection.find(myquery)
    houses_list = []
    for i in houses:
        new_dict = {"_id": i['_id'], "sahipID": i['sahipID'], "price": i['price'], "adres": i['adres'], "sehir": i['sehir'], "long": i['long'], "lat": i['lat'], "image_url": i['image_url'],
                    "desc": i['desc'], "title": i['title']}
        houses_list.append(new_dict)
    output_json = json_util.dumps(houses_list)
    return output_json


@app.route('/getHousesByCity')
def getHousesByCity():
    input_json = request.get_json()
    keyword = input_json['keyword']
    myquery = {"sehir": keyword}
    houses = house_collection.find(myquery)
    houses_list = []
    for i in houses:
        new_dict = {"_id": i['_id'], "sahipID": i['sahipID'], "price": i['price'], "adres": i['adres'], "sehir": i['sehir'], "long": i['long'], "lat": i['lat'], "image_url": i['image_url'],
                    "desc": i['desc'], "title": i['title']}
        houses_list.append(new_dict)
    output_json = json_util.dumps(houses_list)

    return output_json


@app.route('/gethouses', methods=['POST'])
def gethouses():

    input_json = request.get_json()
    #start_date_input = input_json['start_date']
    #end_date_input = input_json['end_date']
    keyword = input_json['keyword']
    #start_date = datetime.datetime(start_date_input['year'], start_date_input['month'], start_date_input['day'])
    #end_date = datetime.datetime(end_date_input['year'], end_date_input['month'], end_date_input['day'])


    search_list = [{"desc": {"$regex": ".*"+keyword+".*"}}, {"title": {"$regex": ".*"+keyword+".*"}}, {"sehir": {"$regex": ".*"+keyword+".*"}}]
    houses = house_collection.find({"$or": search_list})
    houses_list = []
    for i in houses:
        houses_list.append(i)

    output_json = json_util.dumps(houses_list)


    return make_response(output_json, 200)



if __name__ == "__main__":
    app.run(host=host, port=int(port), debug=True)