def format_success(data, message="Success", metadata=None):
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    if metadata:
        response["metadata"] = metadata
    return response

def format_error(error_message, status_code=500, details=None):
    response = {
        "success": False,
        "error": error_message
    }
    if details is not None:
        response["details"] = details
    return response, status_code
