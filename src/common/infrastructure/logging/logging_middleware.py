import os
import logging
import json
import time

from fastapi import Request
from logtail import LogtailHandler

better_stack_url = os.getenv("BETTER_STACK_URL")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logtail = LogtailHandler(better_stack_url)
logger.addHandler(logtail)


async def log_request_response(request: Request, call_next):
    start_time = time.time()

    # Read request body only once
    body = await request.body()

    response = await call_next(request)
    process_time = time.time() - start_time

    # Get query parameters
    query_params = dict(request.query_params)

    # Get path parameters
    path_params = request.path_params

    try:
        body_json = json.loads(body.decode('utf-8'))
    except json.JSONDecodeError:
        body_json = None

    log_details = {
        "method": request.method,
        "url": request.url.path,
        "query_params": query_params,
        "path_params": path_params,
        "status_code": response.status_code,
        "process_time": process_time,
        "client_ip": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        # Response has private children data, can't be sent to better tack to protect sensitive data
        # "request_body": body_json,
        # "response_body": response,
    }

    # Serialize log details to JSON string
    log_message = json.dumps(log_details)

    # Determine log level based on response status code
    if 200 <= response.status_code < 300:
        logger.info(log_message)
    elif 400 <= response.status_code < 500:
        logger.warning(log_message)
    elif 500 <= response.status_code < 600:
        logger.error(log_message)
    else:
        logger.debug(log_message)

    return response
