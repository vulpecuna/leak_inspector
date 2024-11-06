import os

import breachdirectory
import json
import utils.logs


def get(args, target_email):
    log_file_path = f'local/log/breachdirectory/{target_email}.json'

    if not os.path.isfile(log_file_path):
        api_endpoint = "https://breachdirectory.p.rapidapi.com/"
        params = {
            "func": "auto",
            "term": target_email
        }

        data = breachdirectory.handle_api_request(args, api_endpoint, params, log_file_path, {
            'result': []
        })
    else:
        utils.logs.ok(f"Read {log_file_path}")
        with open(log_file_path, 'r') as json_file:
            data = json.loads(json_file.read())

    passwords = []
    hashes = []
    for result in data['result']:
        if 'password' not in result:
            continue
        passwords.append(result['password'] + ':' + result['sha1'])
        hashes.append(result['hash'])

    args.manager.push('breachdirectory', 'passwords', passwords)
    args.manager.push('breachdirectory', 'hashes', hashes)

    return passwords, hashes