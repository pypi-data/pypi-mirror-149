from flask import request
from flask_restx import Resource, fields, reqparse
from ...db.db_connection import database_access
from ...namespace import api
import logging
from ...response_helper import get_response
import json
from bson import json_util

get_rolesPrivileges = reqparse.RequestParser()
get_rolesPrivileges.add_argument("role_name", type=str, required=True)

delete_rolesPrivileges = reqparse.RequestParser()
delete_rolesPrivileges.add_argument("role_name", type=str, required=True)

post_rolesPrivileges = api.model("AddRolePrivileges", {
	"dashboard": fields.String,
	"role_name": fields.String,
	"privileges": fields.Raw(
		[],
		required="true",
		example=[
			{
				"roles": [
					{
						"read": "true",
						"write": "false"
					}
				]
			},
			{
				"create_violation": [
					{
						"read": "true",
						"write": "true"
					}
				]
			},
			{
				"customize_form": [
					{
						"read": "true",
						"write": "true"
					}
				]
			},
			{
				"view_users": [
					{
						"read": "true",
						"write": "true"
					}
				]
			},
			{
				"fingerprint_auth": [
					{
						"read": "true",
						"write": "false"
					}
				]
			},
			{
				"add-new-profile": [
					{
						"read": "true",
						"write": "false"
					}
				]
			},
			{
				"edit-profile": [
					{
						"read": "true",
						"write": "false"
					}
				]
			},
			{
				"view-profiles": [
					{
						"read": "true",
						"write": "false"
					}
				]
			},
			{
				"view-profile": [
					{
						"read": "true",
						"write": "false"
					}
				]
			}
		]
	)
})


class AddRolePrivileges(Resource):
	@api.expect(get_rolesPrivileges)
	def get(self):
		try:
			args = get_rolesPrivileges.parse_args()
			database_connection = database_access()
			rolesPrivileges_col = database_connection["roles&privileges"]
			data = rolesPrivileges_col.find_one({"role_name": args["role_name"]})
			if data:
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Find Roles and Privileges'
			logging.error(e)
			return _response

	@api.expect(post_rolesPrivileges)
	def post(self):
		args = request.get_json()
		try:
			database_connection = database_access()
			rolesPrivileges_col = database_connection["roles&privileges"]
			rolesPrivileges_col.insert_one(
				{"dashboard": args["dashboard"], "role_name": args["role_name"], "privileges": args["privileges"]})
			logging.info(get_response(200))
			return get_response(200)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Roles and Privileges'
			logging.error(e)
			return _response

	@api.expect(post_rolesPrivileges)
	def put(self):
		args = request.get_json()
		try:
			database_connection = database_access()
			rolesPrivileges_col = database_connection["roles&privileges"]
			data = rolesPrivileges_col.find_one({"role_name": args["role_name"]})
			if data:
				rolesPrivileges_col.update_one({"role_name": args["role_name"]}, {'$set': {"privileges": args["privileges"], "dashboard": args["dashboard"]}})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(404))
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Update Roles and Privileges'
			logging.error(e)
			return _response

	@api.expect(delete_rolesPrivileges)
	def delete(self):
		args = delete_rolesPrivileges.parse_args()
		try:
			database_connection = database_access()
			rolesPrivileges_col = database_connection["roles&privileges"]
			data = rolesPrivileges_col.find_one({"role_name": args["role_name"]})
			if data:
				rolesPrivileges_col.delete_one({"role_name": args["role_name"]})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(404))
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Delete Roles and Privileges'
			logging.error(e)
			return _response


class GetAllRolesPrivileges(Resource):
	def get(self):
		try:
			database_connection = database_access()
			rolesPrivileges_col = database_connection["roles&privileges"]
			data = rolesPrivileges_col.find()
			if len(list(data)):
				_response = get_response(200)
				data = rolesPrivileges_col.find()
				print(data)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Find Roles and Privileges'
			logging.error(e)
			return _response
