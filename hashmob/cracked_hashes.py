import hashlib

import hashmob
import json
import os
import utils.logs


def get(args, target_hash):
    log_file_path = f'local/log/hashmob/{hashlib.md5(target_hash.encode()).hexdigest()}.json'

    if not os.path.isfile(log_file_path):
        api_endpoint = 'https://hashmob.net/api/v2/search'
        params = {
            'hashes': [target_hash]
        }
        data = hashmob.handle_api_request(args, api_endpoint, params, log_file_path, {
            'data': {
                'found': []
            }
        })
    else:
        utils.logs.ok(f"Read {log_file_path}")
        with open(log_file_path, 'r') as json_file:
            data = json.loads(json_file.read())

    passwords = []
    for hash_found in data['data']['found']:
        passwords.append(hash_found['plain'])

    args.manager.push('hashmob', 'passwords', passwords)
    return passwords
