import json
import requests
import utils.logs


def handle_api_request(args, api_endpoint, params, log_file_path, default, pro=False):
    # Return an empty result
    if not args.leakcheck_enabled:
        return default

    headers = {}
    if pro:
        headers['X-API-Key'] = ''

    response = requests.get(api_endpoint,
                            params=params, headers=headers)

    try:
        data = response.json()
    except json.JSONDecodeError:
        utils.logs.error(f"Error, received '{response.text}'.", True)

    utils.logs.save_log(log_file_path, data, 1)

    return data