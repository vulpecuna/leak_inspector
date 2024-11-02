import json
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
            # Store the passwords
            if len(passwords) > 0:
                result[original_email] = passwords

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
        for email in entry['emails']:
            if email in result:
                passwords.extend(result[email])
            if email in added_emails:
                emails.extend(added_emails[email])

        entry['passwords'] = passwords
        entry['emails'] = list(set(emails))

    # Save everything
    with open('local/output.json', 'w') as file_data:
        json.dump(data, file_data, indent=4)
