from flask import request
from flask_restx import Resource, reqparse, fields
from ...db.db_connection import database_access
from ...namespace import api
import logging
from ...response_helper import get_response
import json
from bson import json_util

get_violations_employee = reqparse.RequestParser()
get_violations_employee.add_argument("person_id", type=str, required=True, help="Person_ID")

post_violations_employee = api.model("PersonAdd", {
    "person_id": fields.String,
    "violations": fields.Raw(
        [],
        required=True,
        example=[
            {
                "violation_name": "string",
                "comments": "string",
                "date": "string",
            },
        ]
    )
})


class ViolationsEmployee(Resource):
    @api.expect(get_violations_employee)
    def get(self):
        try:
            database_connection = database_access()
            person_violations_col = database_connection["person_violations"]
            args = get_violations_employee.parse_args()
            data = person_violations_col.find_one({"person_id": args["person_id"]})
            _response = get_response(200)
            if data:
                _response["data"] = json.loads(json_util.dumps(data))
                return _response
            else:
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Find Violation'
            logging.error(e)
            return _response

    @api.expect(post_violations_employee)
    def post(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            person_violations_col = database_connection["person_violations"]
            if person_violations_col.find_one({"person_id": args["person_id"]}):
                person_violations_col.update_one({"person_id": args["person_id"]}, {"$push": {"violations": args["violations"][0]}})
                logging.info(get_response(200))
                return get_response(200)
            else:
                person_violations_col.insert_one({"person_id": args["person_id"], "violations": args["violations"]})
                logging.info(get_response(200))
                return get_response(200)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Store Violation'
            logging.error(e)
            return _response