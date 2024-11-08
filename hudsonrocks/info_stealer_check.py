import hudsonrocks
import json
import os
import utils.logs


def get(args, target_email):
    log_file_path = f'local/log/hudsonrocks/{target_email}.json'

    if not os.path.isfile(log_file_path):
        api_endpoint = 'https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email'
        params = {
            'email': target_email
        }

        data = hudsonrocks.handle_api_request(args, api_endpoint, params, log_file_path, None)
    else:
        utils.logs.ok(f"Read {log_file_path}")
        with open(log_file_path, 'r') as json_file:
            data = json.loads(json_file.read())

    if "This email address is not associated with a computer infected by an info-stealer." not in data['message']:
        value = data
    else:
        value = None

    args.manager.push('hudsonrocks', 'info_stealer', value)
