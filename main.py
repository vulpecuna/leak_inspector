import json
import hudsonrocks.info_stealer_check
import leakcheck.breaches_details
import proxynova.leaked_passwords
import utils.args
import utils.logs

args = utils.args.parse()

emails = args.emails
emails_next = {}
emails_done = []
added_emails = {}
result = {}

try:
    while emails:
        # Iterate all emails
        for original_email, email_to_test in emails:
            passwords, new_emails = proxynova.leaked_passwords.get(args, email_to_test)
            info_stealer = hudsonrocks.info_stealer_check.get(args, email_to_test)
            breaches, is_password_exposed = leakcheck.breaches_details.get(args, email_to_test)

            if original_email not in result:
                result[original_email] = {}

            # Store the passwords
            if len(passwords) > 0:
                if 'password' not in result[original_email]:
                    result[original_email]['passwords'] = []
                result[original_email]['passwords'].extend(passwords)

            # Store the stealer data
            if info_stealer is not None:
                if 'info_stealer' not in result[original_email]:
                    result[original_email]['info_stealer'] = []
                result[original_email]['info_stealer'].extend(info_stealer['stealers'])

            # Store the breach details
            if 'breaches' not in result[original_email]:
                result[original_email]['breaches'] = {
                    'password_leaked': False,
                    'list': []
                }
            if is_password_exposed:
                result[original_email]['breaches']['password_leaked'] = True
            result[original_email]['breaches']['list'].extend(breaches)

            # Add the new email candidates
            if len(new_emails) > 0:
                emails_next[original_email] = new_emails

        # When the loop is done, we need to extract the prepare emails to test
        emails_done.extend([v for k, v in emails])
        emails = []
        for next_src, next_value in emails_next.items():
            for email in next_value:
                if email in emails_done:
                    continue
                emails.append((next_src, email))

                # Keep track of added email to add them to the output
                if next_src not in added_emails:
                    added_emails[next_src] = []
                added_emails[next_src].append(email)
    emails_next = {}
finally:
    leakcheck_message = False
    final_result = []
    for input_file in args.sources:
        with open(input_file, 'r') as file:
            data = json.load(file)

            for entry in data['emails']:
                passwords = []
                emails = entry['emails']
                info_stealer = []
                breaches = []
                is_password_exposed = False
                for email in entry['emails']:
                    if email in result:
                        if 'passwords' in result[email]:
                            passwords.extend(result[email]['passwords'])
                        if 'info_stealer' in result[email]:
                            info_stealer.extend(result[email]['info_stealer'])
                        if 'breaches' in result[email]:
                            is_password_exposed = result[email]['breaches']['password_leaked']
                            breaches.extend(result[email]['breaches']['list'])
                    if email in added_emails:
                        emails.extend(added_emails[email])

                entry['passwords'] = passwords
                entry['emails'] = list(set(emails))
                entry['info_stealer'] = info_stealer
                entry['breaches'] = breaches

                if is_password_exposed and len(passwords) == 0:
                    if not leakcheck_message:
                        utils.logs.info(f"You can view additional censored passwords (for free) at "
                                        f"'https://leakcheck.io' for at least one email.")
                        leakcheck_message = True
                    utils.logs.warning(f"[LEAKCHECK] Password was exposed in breaches, not none were found for: {entry['id']} ({entry['emails']})")

            final_result.extend(data['emails'])

    # Save everything
    with open('local/output.json', 'w') as file_data:
        unique_objects = list({obj["id"]: obj for obj in final_result if len(obj["passwords"]) > 0 or
                               len(obj["info_stealer"]) > 0}.values())
        json.dump(unique_objects, file_data, indent=4)
