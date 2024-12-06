import logging
from datetime import datetime
import re


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("ShopeeIntegration")
    return logger

def json_response(status_code, message, data=None, log_level="info"):
    """
    Generate a standard JSON response for API endpoints and log the response.

    :param status_code: HTTP status code to be returned.
    :param message: Message describing the response (e.g., success, error).
    :param data: Data to be included in the response (optional).
    :param logger: Logger instance to log the response (optional).
    :param log_level: Log level (e.g., 'info', 'warning', 'error').
    :return: JSON response with status, message, and data.
    """
    # Default logger if not provided
    logger = logging.getLogger(__name__)
    now = datetime.now()

    # Log the response at the specified log level
    if log_level.lower() == "info":
        logger.info(f"{now} -  Status Code: {status_code} - Message: {message} - Data: {data if data is not None else {}}")
    elif log_level.lower() == "warning":
        logger.warning(f"{now} - Status Code: {status_code} - Message: {message} - Data: {data if data is not None else {}}")
    elif log_level.lower() == "error":
        logger.error(f"{now} - Status Code: {status_code} - Message: {message} - Data: {data if data is not None else {}}")
    else:
        logger.debug(f"{now} - Status Code: {status_code} - Message: {message} - Data: {data if data is not None else {}}")

    # Prepare the response
    response = {
        "status_code": status_code,
        "message": message,
        "data": data if data is not None else {}
    }

    return response

def validate_email(email: str) -> bool:
    """Validasi format email menggunakan regex."""
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

def validate_password(password: str) -> bool:
    """Validasi password minimal 6 karakter, dan mengandung angka dan huruf kapital."""
    return len(password) >= 6 and re.search(r"[A-Z]", password) and re.search(r"\d", password)
