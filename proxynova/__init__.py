import json
import os
import requests
import time
import utils.logs


def handle_api_request(args, api_endpoint, params, log_file_path):
    response = requests.get(api_endpoint,
                            params=params)

    if response.status_code == 502:
        utils.logs.info(f"Received 502 Bad Gateway for {log_file_path}.")
        time.sleep(5)
        return handle_api_request(args, api_endpoint, params, log_file_path)

    try:
        data = response.json()
    except json.JSONDecodeError:
        utils.logs.error(f"Error, received '{response.text}'.", True)

    if 'exception_message' in data and "No alive nodes." in data['exception_message']:
        utils.logs.info(f"Rate limit exceeded when fetching {log_file_path}.")
        time.sleep(15)
        return handle_api_request(args, api_endpoint, params, log_file_path)

    utils.logs.save_log(log_file_path, data, 1)

    return data
