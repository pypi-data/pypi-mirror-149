import traceback


def get_response(code):
    responses = {
        200: {"success": True, "message": "Success", "http_code": 200},
        400: {"success": False, "message": "Bad Request", "http_code": 400},
        401: {"success": False, "message": "Invalid Credentials", "http_code": 401},
        404: {"success": False, "message": "User Doesn't Exists", "http_code": 404},
        405: {"success": False, "message": "Method Not Allowed", "http_code": 405},
        409: {"success": False, "message": "User Already Exist", "http_code": 409},
        500: {
            "success": False,
            "message": "Internal Server Error",
            "http_code": 500,
        },
    }
    if code == 500:
        traceback.print_exc()
    return responses[code]
