from flask import jsonify
from flask_restx import Resource, reqparse
import base64
from ...db.db_connection import database_access
from PIL import Image
from io import BytesIO
from ...namespace import api
import logging
from werkzeug.datastructures import FileStorage
from ...response_helper import get_response

post_driver = reqparse.RequestParser()
post_driver.add_argument("driver_id", type=str, required=True, location="form", help="Driver Id")
post_driver.add_argument("driver_name", type=str, location="form", help="Driver Name")
post_driver.add_argument("licence_no", type=str, location="form", help="Licence Number")
post_driver.add_argument("status", type=str, location="form", help="status")
post_driver.add_argument("image", type=FileStorage, location="files", required=True, help="Select Image")

get_driver = reqparse.RequestParser()
get_driver.add_argument("driver_id", type=str, required=True, help="Driver Id")
get_driver.add_argument("image_name", type=str, help="Image Saved As")

delete_driver = reqparse.RequestParser()
delete_driver.add_argument("driver_id", type=str, required=True, help="Driver Id")


class Driver(Resource):
    @api.expect(get_driver)
    def get(self):
        try:
            database_connection = database_access()
            dms_fingerprint_col = database_connection["dms_fingerprint"]
            args = get_driver.parse_args()
            coll = dms_fingerprint_col.find_one({"driver_id": args["driver_id"]})
            if coll:
                if args["image_name"]:
                    image = Image.open(BytesIO(base64.b64decode(coll["image"])))
                    image.save(args["image_name"])
                logging.info(get_response(200))
                return jsonify(
                    {"driver id": coll["driver_id"], "driver_name": coll["driver_name"],
                     "licence_no": coll["licence_no"], "status": coll["status"]})
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Find Driver Details'
            logging.error(e)
            return _response

    @api.expect(post_driver)
    def post(self):
        args = post_driver.parse_args()
        try:
            database_connection = database_access()
            dms_fingerprint_col = database_connection["dms_fingerprint"]
            data = dms_fingerprint_col.find_one({"driver_id": args["driver_id"]})
            if not data:
                image_string = base64.b64encode(args["image"].read())
                dms_fingerprint_col.insert_one(
                    {"image": image_string, "driver_id": args["driver_id"], "driver_name": args["driver_name"],
                     "licence_no": args["licence_no"],
                     "status": args["status"]})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.error(get_response(406))
                return get_response(406)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Store Driver Details'
            logging.error(e)
            return _response

    @api.expect(post_driver)
    def put(self):
        args = post_driver.parse_args()
        try:
            database_connection = database_access()
            dms_fingerprint_col = database_connection["dms_fingerprint"]
            image_string = base64.b64encode(args["image"].read())
            if dms_fingerprint_col.find_one({"driver_id": args["driver_id"]}):
                dms_fingerprint_col.update_one({"driver_id": args["driver_id"]}, {
                    '$set': {"image": image_string,
                             "driver_name": args["driver_name"],
                             "licence_no": args["licence_no"],
                             "status": args["status"]}})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Update Driver Details'
            logging.error(e)
            return _response

    @api.expect(delete_driver)
    def delete(self):
        try:
            database_connection = database_access()
            dms_fingerprint_col = database_connection["dms_fingerprint"]
            args = delete_driver.parse_args()
            coll = dms_fingerprint_col.find_one({"driver_id": args["driver_id"]})
            if coll:
                dms_fingerprint_col.delete_one({'driver_id': args["driver_id"]})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Delete Driver Details'
            logging.error(e)
            return _response


get_status = reqparse.RequestParser()
get_status.add_argument("driver_id", type=str, required=True, help="Driver Id")

put_status = reqparse.RequestParser()
put_status.add_argument("driver_id", type=str, required=True, location="form", help="Driver Id")
put_status.add_argument("status", type=str, required=True, location="form", help="Status")


class Status(Resource):

    @api.expect(get_status, validate=True)
    def get(self):
        try:
            database_connection = database_access()
            dms_fingerprint_col = database_connection['dms_fingerprint']
            args = get_status.parse_args()
            coll = dms_fingerprint_col.find_one({"driver_id": args["driver_id"]})
            if coll:
                return jsonify({"status": coll["status"]})
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Find Driver Details'
            logging.error(e)
            return _response

    @api.expect(put_status, validate=True)
    def put(self):
        try:
            database_connection = database_access()
            dms_fingerprint_col = database_connection['dms_fingerprint']
            args = put_status.parse_args()
            collection = dms_fingerprint_col.find_one({"driver_id": args["driver_id"]})
            if args["status"] == "enable" and collection["status"] == "enable":
                return jsonify("Status Already enable")
            elif args["status"] == "disable" and collection["status"] == "disable":
                return jsonify("Status Already disable")
            else:
                dms_fingerprint_col.update_one({"driver_id": args["driver_id"]}, {
                    '$set': {"status": args["status"]}})
                logging.info(get_response(200))
                return get_response(200)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Update Driver Details'
            logging.error(e)
            return _response