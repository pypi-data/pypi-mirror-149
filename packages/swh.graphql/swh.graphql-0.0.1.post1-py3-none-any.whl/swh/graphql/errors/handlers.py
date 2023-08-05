def format_error(error) -> dict:
    """
    Response error formatting
    """
    formatted = error.formatted
    formatted["message"] = "Unknown error"
    return formatted
