import json
import cavalier.info_stealer_check
import proxynova.email_leaks
import utils.args

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
            passwords, new_emails = proxynova.email_leaks.get(args, email_to_test)
            info_stealer = cavalier.info_stealer_check.get(args, email_to_test)

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
    with open(args.input_file, 'r') as file_data:
        data = json.load(file_data)

    for entry in data['emails']:
        passwords = []
        emails = entry['emails']
        info_stealer = []
        for email in entry['emails']:
            if email in result:
                if 'passwords' in result[email]:
                    passwords.extend(result[email]['passwords'])
                if 'info_stealer' in result[email]:
                    info_stealer.extend(result[email]['info_stealer'])
            if email in added_emails:
                emails.extend(added_emails[email])

        entry['passwords'] = passwords
        entry['emails'] = list(set(emails))
        entry['info_stealer'] = info_stealer

    # Save everything
    with open('local/output.json', 'w') as file_data:
        json.dump(data, file_data, indent=4)
