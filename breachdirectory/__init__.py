import requests
import utils.logs


def handle_api_request(args, api_endpoint, params, log_file_path, default):
    # Return an empty result
    if not args.breach_directory_api_key:
        return default

    headers = {
        "x-rapidapi-key": args.breach_directory_api_key,
        "x-rapidapi-host": "breachdirectory.p.rapidapi.com"
    }
    response = requests.get(api_endpoint, headers=headers, params=params)
    data = response.json()

    utils.logs.save_log(log_file_path, data, 1)

    return data
