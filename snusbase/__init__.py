import json
import requests
import utils.logs


def handle_api_request(args, api_endpoint, payload, log_file_path, default):
    # Return an empty result
    if not args.snusbase_api_key:
        return default

    response = requests.post(api_endpoint, json=payload, headers={
        'Auth': args.snusbase_api_key
    })

    if response.status_code == 401:
        utils.logs.error(f"Invalid or missing API key for Snusbase.", True)

    if response.status_code == 403:
        utils.logs.error(f"Rate limit exceeded when fetching {log_file_path}\n{response.headers}.", True)

    try:
        data = response.json()
    except json.JSONDecodeError:
        utils.logs.error(f"Error, received '{response.text}'.", True)

    utils.logs.save_log(log_file_path, data, 1)

    return data