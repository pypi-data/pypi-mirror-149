import logging
from flask import request
from flask_restx import Resource, fields
from ...namespace import api
from ...response_helper import get_response

super_login = api.model("SuperLogin", {"password": fields.String})
role = "super_admin"
dashboard="both_dashboard"
first_name="Admin"
privileges = [
    {
		"Roles_Privileges": [
			{
				"read": "true",
				"write": "true"
			}
		]
    }
    , {
		"Users": [
			{
				"read": "true",
				"write": "true"
			}
		]
	},
    {
		"Create_Violation": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Customize_Form": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Fingerprint_Authentication": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Fingerprint_Enrollment": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Add_New_Profile": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"View_Profiles": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Edit_Profile": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Person_Profile": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}]


class SuperLogin(Resource):
	@api.expect(super_login, validate=True)
	def post(self):
		args = request.get_json()
		try:
			password = "Datamoulds@987"
			if args["password"] == password:
				_response = get_response(200)
				_response["role"] = role
				_response["first_name"] = first_name
				_response["dashboard"] = dashboard
				_response["privileges"] = privileges
				return _response
			else:
				logging.error(get_response(401))
				return get_response(401)
		except Exception as e:
			logging.error(e)
