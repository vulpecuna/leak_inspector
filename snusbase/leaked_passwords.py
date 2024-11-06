import hashlib
import json
import os
import snusbase
import utils.logs


def _get_password(args, password_hash):
    password_hash = password_hash.strip()
    hash_log_file_path = f'local/log/snusbase/hashes/{hashlib.md5(password_hash.encode()).hexdigest()}.json'

    if not os.path.isfile(hash_log_file_path):
        api_endpoint = 'https://api.snusbase.com/tools/hash-lookup'
        payload = {
            "terms": [password_hash],
            "types": ["hash"]
        }
        data = snusbase.handle_api_request(args, api_endpoint, payload, hash_log_file_path, {
            'results': {}
        })
    else:
        utils.logs.ok(f"Read {hash_log_file_path}")
        with open(hash_log_file_path, 'r') as json_file:
            data = json.loads(json_file.read())

    for _, breach_data in data['results'].items():
        for entry in breach_data:
            if 'password' in entry:
                return entry['password']
    return None


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
                c = _get_password(args, entry['hash'])
                if c is not None:
                    passwords.append(c)
                    continue
                elif 'salt' in entry:
                    c = entry['salt'] + ':' + entry['hash']
                else:
                    c = entry['hash']
                hashes.append(c.strip())

    args.manager.push('snusbase', 'passwords', passwords)
    args.manager.push('snusbase', 'hashes', hashes)
