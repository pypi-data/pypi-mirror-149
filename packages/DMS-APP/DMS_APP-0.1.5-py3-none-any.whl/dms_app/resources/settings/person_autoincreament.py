from flask_restx import Resource, fields
from ...db.db_connection import database_access
from ...namespace import api
import logging
from ...response_helper import get_response
import pymongo
post_person_id = api.model("AutoIncrement", {
    "person_id_auto_increment": fields.String,
})


class PersonIdAutoIncrement(Resource):
    def get(self):
        try:
            database_connection = database_access()
            user_collection = database_connection["person_profile"]
            data = user_collection.find().sort("_id", pymongo.DESCENDING).limit(1)
            last_data = list(data)[0]['person'][0]['person_id']
            is_digit = ''.join(filter(lambda i: i.isdigit(), last_data))
            increment_digit = int(is_digit)+1
            isalpha = ''.join(filter(lambda i: i.isalpha(), last_data))
            _response = get_response(200)
            _response['person_id'] = isalpha + str(increment_digit)
            logging.info(get_response(200))
            return _response
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Find Person'
            logging.error(e)
            return _response
