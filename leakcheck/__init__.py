import json
import requests
import utils.logs


def handle_api_request(args, api_endpoint, params, log_file_path, default):
    # Return an empty result
    if not args.leakcheck_enabled:
        return default

    response = requests.get(api_endpoint,
                            params=params)

    try:
        data = response.json()
    except json.JSONDecodeError:
        utils.logs.error(f"Error, received '{response.text}'.", True)

    utils.logs.save_log(log_file_path, data, 1)

    return data