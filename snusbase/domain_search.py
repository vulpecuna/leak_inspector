import json
import os
import snusbase
import utils.logs


def get(args, target_domain):
    log_file_path = f'local/log/snusbase/{target_domain}.json'

    if not os.path.isfile(log_file_path):
        api_endpoint = 'https://api.snusbase.com/data/search'
        payload = {
            "terms": [target_domain],
            "types": ["_domain"]
        }

        data = snusbase.handle_api_request(args, api_endpoint, payload, log_file_path, {
            'results': {}
        })
    else:
        utils.logs.ok(f"Read {log_file_path}")
        with open(log_file_path, 'r') as json_file:
            data = json.loads(json_file.read())

    emails = []
    for _, breach_data in data['results'].items():
        for entry in breach_data:
            if 'email' in entry:
                emails.append(entry['email'])
    return list(set(emails))
