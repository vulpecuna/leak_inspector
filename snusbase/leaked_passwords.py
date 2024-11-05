import json
import os
import snusbase
import utils.logs


def get(args, target_email):
    log_file_path = f'local/log/snusbase/{target_email}.json'

    if not os.path.isfile(log_file_path):
        api_endpoint = 'https://api.snusbase.com/data/search'
        payload = {
            "terms": [target_email],
            "types": ["email"]
        }

        data = snusbase.handle_api_request(args, api_endpoint, payload, log_file_path, {
            'results': {}
        })
    else:
        utils.logs.ok(f"Read {log_file_path}")
        with open(log_file_path, 'r') as json_file:
            data = json.loads(json_file.read())

    breaches = data['results']
    passwords = []
    hashes = []
    for _, breach_data in breaches.items():
        for entry in breach_data:
            if 'password' in entry:
                passwords.append(entry['password'])
            if 'hash' in entry:
                c = entry['hash']
                if 'salt' in entry:
                    c = entry['salt'] + ':' + entry['hash']
                hashes.append(c.strip())

    return passwords, hashes
