import os
import proxynova
import json
import utils.logs

already_checked = []


def get(args, target_email):
    log_file_path = f'local/log/proxynova/{target_email}.json'

    if not os.path.isfile(log_file_path):
        api_endpoint = 'https://api.proxynova.com/comb'
        params = {
            'query': target_email,
            'start': '0',
            'limit': '15',
        }

        data = proxynova.handle_api_request(args, api_endpoint, params, log_file_path, {
            'lines': []
        })
    else:
        utils.logs.ok(f"Read {log_file_path}")
        with open(log_file_path, 'r') as json_file:
            data = json.loads(json_file.read())

    global already_checked
    already_checked.append(target_email)

    passwords = []
    new_emails = []
    for leak in data['lines']:
        if leak.count(':') != 1:
            continue
        [username, password] = leak.split(':')

        # Small patch due to invalid entries
        username = username.replace("@@", "@")

        # Found a password for this email
        # Or found another similar email with the same password
        # (in practice, we should widen the concept of "same")
        if username == target_email:
            passwords.append(password)
        elif password in passwords:
            # Best effort to not check an email twice (+ the warning)
            if username in already_checked:
                continue

            new_username, known_username = username.split('@')[0], target_email.split('@')[0]
            if new_username == known_username:
                utils.logs.warning(f"Found another email with the same password? ({username} for {target_email}")
                new_emails.append(username)
                already_checked.append(username)

    args.manager.push('proxynova', 'passwords', passwords)
    args.manager.push('proxynova', 'new_emails', new_emails)
