from flask_restx import Resource, reqparse
from ...db.db_connection import database_access
from ...namespace import api
from ...response_helper import get_response
import json
from bson import json_util
import logging
import re

# logging.basicConfig(filename='info.log', level=logging.INFO, format='%(asctime)s %(message)s')

search_employee = reqparse.RequestParser()
search_employee.add_argument("person_name", type=str, required=True, help="Person Name")


class SearchEmployee(Resource):
    @api.expect(search_employee)
    def get(self):
        try:
            database_connection = database_access()
            person_profile_col = database_connection["person_profile"]
            args = search_employee.parse_args()
            regx = re.compile(args["person_name"], re.IGNORECASE)
            data = person_profile_col.find({"person.name": {'$regex': regx}})
            if len(list(data)):
                logging.info(get_response(200))
                _response = get_response(200)
                data = person_profile_col.find({"person.name": {'$regex': regx}})
                _response["data"] = json.loads(json_util.dumps(data))
                return _response
            else:
                logging.info(get_response(404))
                _response = get_response(404)
                return _response
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Get Employee Detail'
            logging.error(e)
            return _response
