from flask import request
from flask_restx import Resource, reqparse, fields
from ...db.db_connection import database_access
from ...namespace import api
import logging
from ...response_helper import get_response
import json
from bson import json_util

get_employee = reqparse.RequestParser()
get_employee.add_argument("person_id", type=str, required=True, help="Person_ID")

get_all_employee = reqparse.RequestParser()
get_all_employee.add_argument("page_no", type=int, required=True, help="Page number")
get_all_employee.add_argument("page_limit", type=int, required=True, help="limit ")

get_emp_status_filter = reqparse.RequestParser()
get_emp_status_filter.add_argument("status", type=str, required=True, help="Status")
get_emp_status_filter.add_argument("page_no", type=int, required=True, help="Page number")
get_emp_status_filter.add_argument("page_limit", type=int, required=True, help="limit ")

delete_profile = api.model("DeleteProfile", {
    "person_id": fields.String
})

add_profile = api.model("ProfileAdd", {
    "person": fields.Raw(
        [],
        required=True,
        example=[
            {
                "person_id": "string",
                "name": "string",
                "role": "string",
                "blacklist": "string",
                "added_by": "string",
                "added_date": "added_date",
                "image": "string",
                "fingerprint": "string",
                "status": "string",
            },
        ]
    )
})


class AddEmployee(Resource):
    @api.expect(get_employee)
    def get(self):
        try:
            database_connection = database_access()
            person_profile_col = database_connection["person_profile"]
            args = get_employee.parse_args()
            person_id = args["person_id"]
            data = person_profile_col.find_one(
                {'person.person_id': {'$regex': '^{person}$'.format(person=person_id), '$options': 'i'}})
            _response = get_response(200)
            if data:
                _response["data"] = json.loads(json_util.dumps(data))
                return _response
            else:
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Get Employee Detail'
            logging.error(e)
            return _response

    @api.expect(add_profile)
    def post(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            person_profile_col = database_connection["person_profile"]
            user = person_profile_col.find_one({"person.person_id": args["person"][0]["person_id"]})
            if not user:
                person_profile_col.insert_one({
                    "person": args["person"]})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.info(get_response(409))
                return get_response(409)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Store Employee'
            logging.error(e)
            return _response

    @api.expect(add_profile)
    def put(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            person_profile_col = database_connection["person_profile"]
            if person_profile_col.find_one({"person.person_id": args["person"][0]["person_id"]}):
                person_profile_col.delete_one({"person.person_id": args["person"][0]["person_id"]})
                person_profile_col.insert_one({"person": args["person"]})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.info(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Update Employee Detail'
            logging.error(e)
            return _response

    @api.expect(delete_profile)
    def delete(self):
        try:
            database_connection = database_access()
            person_profile_col = database_connection["person_profile"]
            add_person_col = database_connection["add_person"]
            args = request.get_json()
            coll = person_profile_col.find_one({"person.person_id": args["person_id"]})
            if coll:
                person_profile_col.delete_one({"person.person_id": args["person_id"]})
                add_person_col.delete_one({"person_id": args["person_id"]})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Delete Employee Detail'
            logging.error(e)
            return _response


class GetEmployee(Resource):
    @api.expect(get_all_employee)
    def get(self):
        try:
            database_connection = database_access()
            person_profile_col = database_connection["person_profile"]
            args = get_all_employee.parse_args()
            count = person_profile_col.count_documents({})
            data = person_profile_col.find()
            if len(list(data)):
                data = person_profile_col.find().skip(args["page_limit"] * (args["page_no"] - 1)).limit(
                    args["page_limit"])
                _response = get_response(200)
                _response['count'] = count
                _response["data"] = json.loads(json_util.dumps(data))
                return _response
            else:
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Get Employee Detail'
            logging.error(e)
            return _response


class EmployeeStatusFilter(Resource):
    @api.expect(get_emp_status_filter)
    def get(self):
        try:
            database_connection = database_access()
            person_profile_col = database_connection["person_profile"]
            args = get_emp_status_filter.parse_args()
            page = args["page_no"]
            page_limit = args["page_limit"]
            data = person_profile_col.find({"person.status": args["status"]})
            if len(list(data)):
                data = person_profile_col.find({"person.status": args["status"]}).skip(page_limit * (page - 1)).limit(
                    page_limit)
                _response = get_response(200)
                _response["data"] = json.loads(json_util.dumps(data))
                return _response
            else:
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Get Employee Detail'
            logging.error(e)
            return _response
