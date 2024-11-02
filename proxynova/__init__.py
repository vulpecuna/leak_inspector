import json
import os
import requests
import time
import utils.logs


def handle_api_request(args, api_endpoint, params, log_file_path):
    response = requests.get(api_endpoint,
                            params=params)

    try:
        data = response.json()
    except json.JSONDecodeError:
        utils.logs.error(f"Error, received {response.text}.", True)

    if 'exception_message' in data and "No alive nodes." in data['exception_message']:
        utils.logs.info(f"Rate limit exceeded when fetching {log_file_path}.")
        time.sleep(15)
        return handle_api_request(args, api_endpoint, params, log_file_path)

    utils.logs.ok(f"Fetched {log_file_path}.")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    time.sleep(1)

    return data
