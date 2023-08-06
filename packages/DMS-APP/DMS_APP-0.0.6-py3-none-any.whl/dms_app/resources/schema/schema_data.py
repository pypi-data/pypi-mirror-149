from flask import request
from flask_restx import Resource, fields
from ...db.db_connection import database_access
from ...namespace import api
import logging
from ...response_helper import get_response
import json
from bson import json_util



post_schema = api.model("SchemaAdd", {
    "schema": fields.Raw(
        [],
        required=True,
        example=[
            {
                "name": "person_id",
                "display_name": "Person ID",
                "data_type": "string",
                "is_required": "false",
                "default_value": "",
                "length": 0,
                "is_unique": "false",
                "is_key": "false",
                "is_hidden": "false",
                "enter_values": "",
                "componentType": "",
                "dateTimeFormat": "%d-%m-%Y"
            },
        ]
    )
})

put_schema = api.model("SchemaUpdate", {
    "name": fields.String,
    "display_name": fields.String,
    "data_type": fields.String,
    "is_required": fields.String,
    "default_value": fields.String,
    "length": fields.Integer,
    "is_unique": fields.String,
    "is_key": fields.String,
    "is_hidden": fields.String,
    "enter_values": fields.String,
    "componentType": fields.String,
    "dateTimeFormat": fields.String
})


class AddSchema(Resource):
    def get(self):
        try:
            database_connection = database_access()
            schema_col = database_connection["schema"]
            coll = schema_col.find()
            if len(list(coll)):
                coll = schema_col.find()
                _response = get_response(200)
                _response["data"] = json.loads(json_util.dumps(coll))
                return _response
            else:
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Get Schema'
            logging.error(e)
            return _response

    @api.expect(post_schema)
    def post(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            schema_col = database_connection["schema"]
            schema_col.delete_many({})
            schema_col.insert_one(
                {"schema": args["schema"]})
            logging.info(get_response(200))
            return get_response(200)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Store Schema'
            logging.error(e)
            return _response

    @api.expect(put_schema)
    def put(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            schema_col = database_connection["schema"]
            if schema_col.find_one({"schema.name": args["name"]}):
                schema_col.update_one({"schema.name": args["name"]},
                                           {'$set': {
                                               "schema.$.display_name": args['display_name'],
                                               "schema.$.data_type": args['data_type'],
                                               "schema.$.is_required": args['is_required'],
                                               "schema.$.default_value": args[
                                                   'default_value'],
                                               "schema.$.length": args['length'],
                                               "schema.$.is_unique": args['is_unique'],
                                               "schema.$.is_key": args['is_key'],
                                               "schema.$.is_hidden": args['is_hidden'],
                                               "schema.$.enter_values": args['enter_values'],
                                               "schema.$.componentType": args[
                                                   'componentType'],
                                               "schema.$.dateTimeFormat": args[
                                                   'dateTimeFormat']}}
                                           )
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.info(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Update Schema'
            logging.error(e)
            return _response
