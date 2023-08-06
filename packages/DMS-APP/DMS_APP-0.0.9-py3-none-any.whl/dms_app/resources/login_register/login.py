# import hashlib
# import logging
# from flask import request
# from ...db.db_connection import database_access
# from flask_restx import Resource, fields, reqparse
# from ...namespace import api
# from ...response_helper import get_response
# import json
# from bson import json_util
# import smtplib
# import re
# from bson.objectid import ObjectId
# from random import *
#
# post_user = api.model("AddUser", {
#     "first_name": fields.String,
#     "last_name": fields.String,
#     "password": fields.String,
#     "email": fields.String,
#     "role": fields.String,
#     "contact": fields.String,
# })
#
# get_all_User = reqparse.RequestParser()
# get_all_User.add_argument("page_no", type=int, required=True, help="Page number")
# get_all_User.add_argument("page_limit", type=int, required=True, help="limit ")
#
# put_user = api.model("PutUser", {
#     "first_name": fields.String,
#     "last_name": fields.String,
#     "email": fields.String,
#     "role": fields.String,
#     "contact": fields.String,
# })
#
# change_user_password = api.model("ChangePassword", {
#     "email": fields.String,
#     "password": fields.String
# })
#
# delete_user = api.model("DeleteUser", {
#     "object_id": fields.String
# })
#
#
# class AddUser(Resource):
#     @api.expect(get_all_User)
#     def get(self):
#         try:
#             args = get_all_User.parse_args()
#             database_connection = database_access()
#             dms_user_col = database_connection["dms_user"]
#             data = dms_user_col.find({}, {"password": 0})
#             count=dms_user_col.count_documents({})
#             if len(list(data)):
#                 logging.info(get_response(200))
#                 _response = get_response(200)
#                 data = dms_user_col.find({}, {"password": 0}).skip(args["page_limit"] *
#                                                                    (args["page_no"]-1)).limit(args["page_limit"])
#                 _response["data"] = json.loads(json_util.dumps(data))
#                 _response["count"]=count
#                 return _response
#             else:
#                 logging.info(get_response(404))
#                 _response = get_response(404)
#                 return _response
#         except Exception as e:
#             logging.error(e)
#
#     @api.expect(post_user, validate=True)
#     def post(self):
#         args = request.get_json()
#         try:
#             database_connection = database_access()
#             dms_user_col = database_connection["dms_user"]
#             recipient = args['email'].strip()
#             password = args["password"]
#             body = "Hello " + args["first_name"] + " " + args["last_name"] + "," + \
#                    "\r\nOne Time Password for Login Driver Management System Application is " + args["password"]
#             hash_password = hashlib.md5(password.encode("utf-8")).digest()
#             server = smtplib.SMTP("smtp.gmail.com", 587)
#             server.starttls()
#             regx = re.compile(args["email"], re.IGNORECASE)
#             if not dms_user_col.find_one({"email": {'$regex': regx}}):
#                 server.login("dmsmail130@gmail.com", "Pratu@12")
#                 server.sendmail('dmsmail130@gmail.com', recipient, body)
#                 dms_user_col.insert_one(
#                     {"first_name": args["first_name"], "last_name": args["last_name"], "email": args["email"],
#                      "password": hash_password, "role": args["role"], "contact": args["contact"]})
#                 logging.info(get_response(200))
#                 return get_response(200)
#             else:
#                 logging.error(get_response(409))
#                 return get_response(409)
#         except Exception as e:
#             logging.error(e)
#
#     @api.expect(put_user, validate=True)
#     def put(self):
#         args = request.get_json()
#         try:
#             database_connection = database_access()
#             dms_user_col = database_connection["dms_user"]
#             regx_email = re.compile(args["email"], re.IGNORECASE)
#             if dms_user_col.find_one({"email": {'$regex': regx_email}}):
#                 dms_user_col.update_one({"email": args["email"]}, {
#                     '$set':
#                         {"first_name": args["first_name"], "last_name": args["last_name"], "email": args["email"],
#                             "role": args["role"], "contact": args["contact"]}})
#                 logging.info(get_response(200))
#                 return get_response(200)
#             else:
#                 logging.error(get_response(404))
#                 return get_response(404)
#         except Exception as e:
#             logging.error(e)
#
#     @api.expect(delete_user, validate=True)
#     def delete(self):
#         args = request.get_json()
#         try:
#             database_connection = database_access()
#             dms_user_col = database_connection["dms_user"]
#             if dms_user_col.find_one({"_id": ObjectId(args["object_id"])}):
#                 dms_user_col.delete_one({"_id": ObjectId(args["object_id"])})
#                 logging.info(get_response(200))
#                 return get_response(200)
#             else:
#                 logging.error(get_response(404))
#                 return get_response(404)
#         except Exception as e:
#             logging.error(e)
#
#
# user_login = api.model("UserLogin", {
#     "email": fields.String,
#     "password": fields.String,
# })
#
#
# class Login(Resource):
#     @api.expect(user_login, validate=True)
#     def post(self):
#         args = request.get_json()
#         print(args)
#         try:
#             database_connection = database_access()
#             dms_user_col = database_connection["dms_user"]
#             regx_email = re.compile(args["email"], re.IGNORECASE)
#             check_email = dms_user_col.find_one({"email": {'$regex': regx_email}})
#             hash_password = hashlib.md5(args["password"].encode('utf-8')).digest()
#             if check_email:
#                 if check_email["password"] == hash_password:
#                     logging.info(get_response(200))
#                     _response = get_response(200)
#                     _response["role"] = json.loads(json_util.dumps(check_email["role"]))
#                     _response["first_name"] = json.loads(json_util.dumps(check_email["first_name"]))
#                     _response["last_name"] = json.loads(json_util.dumps(check_email["last_name"]))
#                     return _response
#                 else:
#                     logging.error(get_response(401))
#                     return get_response(401)
#             else:
#                 logging.error(get_response(404))
#                 return get_response(404)
#         except Exception as e:
#             logging.error(e)
#
#
# search_user = reqparse.RequestParser()
# search_user.add_argument("email", type=str, required=True, help="Email")
#
#
# class SearchUser(Resource):
#     @api.expect(search_user)
#     def get(self):
#         try:
#             database_connection = database_access()
#             dms_user_col = database_connection["dms_user"]
#             args = search_user.parse_args()
#             regx_email = re.compile(args["email"], re.IGNORECASE)
#             data = dms_user_col.find_one({"$or": [{"email": {'$regex': regx_email}},
#                                          {"first_name": {'$regex': regx_email}}]})
#             data=[data]
#             if data:
#                 logging.info(get_response(200))
#                 _response = get_response(200)
#                 _response["data"] = json.loads(json_util.dumps(data))
#                 return _response
#             else:
#                 logging.info(get_response(404))
#                 _response = get_response(404)
#                 return _response
#         except Exception as e:
#             logging.error(e)
#
#
# get_user_role_filter = reqparse.RequestParser()
# get_user_role_filter.add_argument("role", type=str, required=True, help="role")
# get_user_role_filter.add_argument("page_no", type=int, required=True, help="Page number")
# get_user_role_filter.add_argument("page_limit", type=int, required=True, help="limit ")
#
#
# class UserRoleFilter(Resource):
#     @api.expect(get_user_role_filter)
#     def get(self):
#         try:
#             database_connection = database_access()
#             dms_user_col = database_connection["dms_user"]
#             args = get_user_role_filter.parse_args()
#             page = args["page_no"]
#             page_limit = args["page_limit"]
#             data = dms_user_col.find({"role": args["role"]}, {"password": 0})
#             if len(list(data)):
#                 data = dms_user_col.find({"role": args["role"]}, {"password": 0}).skip(page_limit * (page - 1)).limit(
#                     page_limit)
#                 _response = get_response(200)
#                 _response["data"] = json.loads(json_util.dumps(data))
#                 return _response
#             else:
#                 return get_response(404)
#         except Exception as e:
#             logging.error(e)
#
#
# class ChangeUserPassword(Resource):
#     @api.expect(change_user_password, validate=True)
#     def put(self):
#         args = request.get_json()
#         try:
#             database_connection = database_access()
#             dms_user_col = database_connection["dms_user"]
#             hash_password = hashlib.md5(args["password"].encode("utf-8")).digest()
#             regx_email = re.compile(args["email"], re.IGNORECASE)
#             if dms_user_col.find_one({"email": {'$regex': regx_email}}):
#                 dms_user_col.update_one({"email": args["email"]}, {'$set':
#                                                                        {"password": hash_password}})
#                 logging.info(get_response(200))
#                 return get_response(200)
#             else:
#                 logging.error(get_response(409))
#                 return get_response(409)
#         except Exception as e:
#             logging.error(e)

import hashlib
import logging
from flask import request
from ...db.db_connection import database_access
from flask_restx import Resource, fields, reqparse
from ...namespace import api
from ...response_helper import get_response
import json
from bson import json_util
import smtplib
import re
from bson.objectid import ObjectId
from random import *
import random
import math

post_user = api.model("AddUser", {
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "role": fields.String,
    "contact": fields.String,
})

get_all_User = reqparse.RequestParser()
get_all_User.add_argument("page_no", type=int, required=True, help="Page number")
get_all_User.add_argument("page_limit", type=int, required=True, help="limit ")

put_user = api.model("PutUser", {
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "role": fields.String,
    "contact": fields.String,
})

change_user_password = api.model("ChangePassword", {
    "email": fields.String,
    "password": fields.String
})

delete_user = api.model("DeleteUser", {
    "object_id": fields.String
})


class AddUser(Resource):
    @api.expect(get_all_User)
    def get(self):
        try:
            args = get_all_User.parse_args()
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            data = dms_user_col.find({}, {"password": 0})
            count = dms_user_col.count_documents({})
            if len(list(data)):
                logging.info(get_response(200))
                _response = get_response(200)
                data = dms_user_col.find({}, {"password": 0})
                _response["data"] = json.loads(json_util.dumps(data))
                _response["count"] = count
                return _response
            else:
                logging.info(get_response(404))
                _response = get_response(404)
                return _response
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Find User'
            logging.error(e)
            return _response

    @api.expect(post_user, validate=True)
    def post(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            digits = [i for i in range(0, 10)]
            otp = ""
            for i in range(6):
                index = math.floor(random.random() * 10)
                otp += str(digits[index])
            recipient = args['email'].strip()
            body = "Hello " + args["first_name"] + " " + args["last_name"] + "," + \
                   "\r\nOne Time Password for Driver Management System Application : " + str(otp)
            hash_password = hashlib.md5(str(otp).encode("utf-8")).digest()
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            regx = re.compile(args["email"], re.IGNORECASE)
            if not dms_user_col.find_one({"email": {'$regex': regx}}):
                server.login("dmsbackend12@gmail.com", "Dms@1234")
                server.sendmail('dmsbackend12@gmail.com', recipient, body)
                dms_user_col.insert_one(
                    {"first_name": args["first_name"], "last_name": args["last_name"], "email": args["email"],
                     "password": hash_password, "role": args["role"], "contact": args["contact"]})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.error(get_response(409))
                return get_response(409)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Store User'
            logging.error(e)
            return _response

    @api.expect(put_user, validate=True)
    def put(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            regx_email = re.compile(args["email"], re.IGNORECASE)
            if dms_user_col.find_one({"email": {'$regex': regx_email}}):
                dms_user_col.update_one({"email": args["email"]}, {
                    '$set':
                        {"first_name": args["first_name"], "last_name": args["last_name"], "email": args["email"],
                            "role": args["role"], "contact": args["contact"]}})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Update User'
            logging.error(e)
            return _response

    @api.expect(delete_user, validate=True)
    def delete(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            if dms_user_col.find_one({"_id": ObjectId(args["object_id"])}):
                dms_user_col.delete_one({"_id": ObjectId(args["object_id"])})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Delete User'
            logging.error(e)
            return _response


user_login = api.model("UserLogin", {
    "email": fields.String,
    "password": fields.String,
})


class Login(Resource):
    @api.expect(user_login, validate=True)
    def post(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            regx_email = re.compile(args["email"], re.IGNORECASE)
            check_email = dms_user_col.find_one({"email": {'$regex': regx_email}})
            hash_password = hashlib.md5(args["password"].encode('utf-8')).digest()
            if check_email:
                logging.info(get_response(200))
                _response = get_response(200)
                _response["role"] = json.loads(json_util.dumps(check_email["role"]))
                _response["first_name"] = json.loads(json_util.dumps(check_email["first_name"]))
                _response["last_name"] = json.loads(json_util.dumps(check_email["last_name"]))
                if check_email["password"] == hash_password:
                    if len(args["password"]) == 6 and args["password"].isdigit():
                        _response["otp"] = True
                        return _response
                    else:
                        _response["otp"] = False
                        return _response
                else:
                    logging.error(get_response(401))
                    return get_response(401)
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Store User'
            logging.error(e)
            return _response


search_user = reqparse.RequestParser()
search_user.add_argument("email", type=str, required=True, help="Email")


class SearchUser(Resource):
    @api.expect(search_user)
    def get(self):
        try:
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            args = search_user.parse_args()
            regx_email = re.compile(args["email"], re.IGNORECASE)
            data = dms_user_col.find_one({"$or": [{"email": {'$regex': regx_email}},
                                         {"first_name": {'$regex': regx_email}}]})

            if len(data):
                data = [data]
                logging.info(get_response(200))
                _response = get_response(200)
                _response["data"] = json.loads(json_util.dumps(data))
                return _response
            else:
                logging.info(get_response(404))
                _response = get_response(404)
                return _response
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'User Not Found'
            logging.error(e)
            return _response


get_user_role_filter = reqparse.RequestParser()
get_user_role_filter.add_argument("role", type=str, required=True, help="role")
get_user_role_filter.add_argument("page_no", type=int, required=True, help="Page number")
get_user_role_filter.add_argument("page_limit", type=int, required=True, help="limit ")


class UserRoleFilter(Resource):
    @api.expect(get_user_role_filter)
    def get(self):
        try:
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            args = get_user_role_filter.parse_args()
            page = args["page_no"]
            page_limit = args["page_limit"]
            data = dms_user_col.find({"role": args["role"]}, {"password": 0})
            if len(list(data)):
                data = dms_user_col.find({"role": args["role"]}, {"password": 0}).skip(page_limit * (page - 1)).limit(
                    page_limit)
                _response = get_response(200)
                _response["data"] = json.loads(json_util.dumps(data))
                return _response
            else:
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Find User'
            logging.error(e)
            return _response


class ChangeUserPassword(Resource):
    @api.expect(change_user_password, validate=True)
    def put(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            hash_password = hashlib.md5(args["password"].encode("utf-8")).digest()
            regx_email = re.compile(args["email"], re.IGNORECASE)
            if dms_user_col.find_one({"email": {'$regex': regx_email}}):
                dms_user_col.update_one({"email": args["email"]}, {'$set':
                                                                       {"password": hash_password}})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.error(get_response(409))
                return get_response(409)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Update User'
            logging.error(e)
            return _response
