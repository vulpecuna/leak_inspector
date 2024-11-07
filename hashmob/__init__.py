import json
import requests
import utils.logs


def handle_api_request(args, api_endpoint, params, log_file_path, default):
    # Return an empty result
    if not args.hashmob_api_key:
        return default

    response = requests.post(api_endpoint, json=params, headers={"api-key": args.hashmob_api_key})

    try:
        data = response.json()
    except json.JSONDecodeError:
        utils.logs.error(f"Error, received '{response.text}'.", True)

    # The API key is invalid
    if response.status_code == 401:
        utils.logs.error(f"Invalid API key for HashMob.", True)

    # The API must be disabled until it's available to us
    if response.status_code == 402:
        utils.logs.info(f"Rate limit exceeded when fetching {log_file_path}.")
        utils.logs.error(f"Received message {data['error_message']}.")
        args.hashmob_api_key = None
        return default

    utils.logs.save_log(log_file_path, data, 1)

    return data
