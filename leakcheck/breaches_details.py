import json
import leakcheck
import os
import utils.logs


def get(args, target_email):
    log_file_path = f'local/log/leakcheck/breaches/{target_email}.json'

    if not os.path.isfile(log_file_path):
        api_endpoint = 'https://leakcheck.io/api/public'
        params = {
            'check': target_email,
        }

        data = leakcheck.handle_api_request(args, api_endpoint, params, log_file_path, {
            'sources': [],
            'fields': []
        })
    else:
        utils.logs.ok(f"Read {log_file_path}")
        with open(log_file_path, 'r') as json_file:
            data = json.loads(json_file.read())

    return data['sources'] if 'sources' in data else [], 'password' in data['fields'] if 'fields' in data else False