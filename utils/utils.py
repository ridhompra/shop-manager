import logging
from datetime import datetime
import re
from typing import List, Any, Optional, Dict


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("ShopeeIntegration")
    return logger

def json_response(
    status_code: int, 
    message: str, 
    data: Optional[List[Dict[str, Any]]] = None, 
    log_level: str = "info", 
    pagination: Optional[Dict[str, Any]] = None
):
    """
    Generate a standard JSON response for API endpoints and log the response.

    :param status_code: HTTP status code to be returned.
    :param message: Message describing the response (e.g., success, error).
    :param data: Data to be included in the response (optional, defaults to an empty array).
    :param log_level: Log level (e.g., 'info', 'warning', 'error').
    :param pagination: Pagination information (optional, defaults to None).
    :return: JSON response with status_code, message, and data as an array.
    """
    # Default logger setup
    logger = logging.getLogger(__name__)
    now = datetime.now()

    # Ensure data is always a list (array)
    response_data = data if isinstance(data, list) else []

    log_message = f"{now} - Status Code: {status_code} - Message: {message} - Data Count: {len(response_data)}"
    if log_level.lower() == "info":
        logger.info(log_message)
    elif log_level.lower() == "warning":
        logger.warning(log_message)
    elif log_level.lower() == "error":
        logger.error(log_message)
    else:
        logger.debug(log_message)

    response = {
        "status_code": status_code,
        "message": message,
        "data": response_data
    }

    if pagination:
        if isinstance(pagination, dict):
            response["page"] = pagination.get("page", 1)
            response["limit"] = pagination.get("limit", 10)
            response["total"] = pagination.get("total", 0)
            response["total_page"] = pagination.get("total_page", 0)
            response["next"] = pagination.get("next", None)
            response["prev"] = pagination.get("prev", None)
        else:
            logger.warning(f"Invalid pagination format. Expected a dictionary, got {type(pagination)}.")

    return response


def validate_email(email: str) -> bool:
    """Validasi format email menggunakan regex."""
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

def validate_password(password: str) -> bool:
    """Validasi password minimal 6 karakter, dan mengandung angka dan huruf kapital."""
    return len(password) >= 6 and re.search(r"[A-Z]", password) and re.search(r"\d", password)
