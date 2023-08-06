from flask import request
from flask_restx import Resource, fields, reqparse
from ...db.db_connection import database_access
from ...namespace import api
from ...response_helper import get_response
from bson import json_util
import json

createFingerPrint = api.model("CreateFingerprint", {
	"person_id": fields.String,
	"base64str1": fields.String,
	"base64str2": fields.String,
	"base64str3": fields.String,
})

fingerPrintDelete = reqparse.RequestParser()
fingerPrintDelete.add_argument("fingerprint_id", type=int, required=True)

fingerPrintGet = reqparse.RequestParser()
fingerPrintGet.add_argument("person_id", type=str, required=True)


class AddFingerprint(Resource):
	@api.expect(createFingerPrint)
	def post(self):
		args = request.get_json()
		print(args)
		try:
			db_connection = database_access()
			fingerprintCollection = db_connection["sample"]
			data = fingerprintCollection.find()
			db_connection.sample.insert_one({"fingerPrintId": len(list(data)) + 1, "person_id": args["person_id"], "base64str1":
				args["base64str1"], "base64str2": args["base64str2"], "base64str3": args["base64str3"]})
			print('insert')
			return get_response(200)
		except Exception as e:
			print(e)

	@api.expect(fingerPrintGet)
	def get(self):
		try:
			args = fingerPrintGet.parse_args()
			print(args)
			db_connection = database_access()
			fingerprintCollection = db_connection["sample"]
			data = fingerprintCollection.find_one({"person_id":args["person_id"]})
			print(data)
			if data:
				print(data)
				_response = get_response(200)
				data = fingerprintCollection.find({"person_id":args["person_id"]})
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				_response = get_response(404)
				return _response
		except Exception as e:
			print(e)

	# @api.expect(fingerPrintGet)
	# def get(self):
	# 	try:
	# 		args= request.get_json()
	# 		db_connection = database_access()
	# 		fingerprintCollection = db_connection["sample"]
	# 		data = fingerprintCollection.find_one({"fingerPrintId":args["fingerprint_id"]})
	# 		print("sddfs")
	# 		data_dict = get_response(200)
	# 		data_dict["data"] = json.loads(json_util.dumps(data))
	# 		if data:
	# 			return data_dict
	# 		else:
	# 			return get_response(404)
	# 	except Exception as e:
	# 		print(e)

	@api.expect(fingerPrintDelete)
	def delete(self):
		try:
			db_connection = database_access()
			fingerprintCollection = db_connection["sample"]
			args = fingerPrintDelete.parse_args()
			coll = fingerprintCollection.find_one({"fingerPrintId": args["fingerprint_id"]})
			if coll:
				fingerprintCollection.delete_one({"fingerPrintId": args["fingerprint_id"]})
				return get_response(200)
			else:
				return get_response(404)
		except Exception as e:
			print(e)
