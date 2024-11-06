import json
import hudsonrocks.info_stealer_check
import leakcheck.breaches_details
import proxynova.leaked_passwords
import snusbase.domain_search
import snusbase.leaked_passwords
import utils.args
import utils.export
import utils.logs

args = utils.args.parse()

emails = args.emails
emails_next = {}
emails_done = []
added_emails = {}
result = {}

# Compute domain emails
domain_emails = []
if args.domain:
    domain_emails.extend(snusbase.domain_search.get(args, args.domain))
    domain_emails = [(email, email) for email in domain_emails if email not in emails]
    emails.extend(domain_emails)

try:
    while emails:
        # Iterate all emails
        for original_email, email_to_test in emails:
            passwords, new_emails = proxynova.leaked_passwords.get(args, email_to_test)
            info_stealer = hudsonrocks.info_stealer_check.get(args, email_to_test)
            breaches, is_password_exposed = leakcheck.breaches_details.get(args, email_to_test)

            passwords2, hashes = snusbase.leaked_passwords.get(args, email_to_test)
            passwords.extend(passwords2)

            if original_email not in result:
                result[original_email] = {}

            # Store the passwords
            if len(passwords) > 0:
                if 'password' not in result[original_email]:
                    result[original_email]['passwords'] = []
                result[original_email]['passwords'].extend(passwords)

            # Store the hashes
            if len(hashes) > 0:
                if 'hashes' not in result[original_email]:
                    result[original_email]['hashes'] = []
                result[original_email]['hashes'].extend(hashes)

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
            # Update and add each entry
            for entry in data['emails']:
                final_result.append(utils.export.compute_entry(entry, result, added_emails))

    # Add new entries
    for domain_email in domain_emails:
        k, _ = domain_email
        final_result.append(utils.export.compute_entry({
            "id": k,
            "first_name": None,
            "last_name": None,
            "emails": [
                k
            ]
        }, result, added_emails))

    # Save everything without duplicates
    with open('local/output.json', 'w') as file_data:
        unique_objects = list({obj["id"]: obj for obj in final_result if len(obj["passwords"]) > 0 or
                               len(obj["hashes"]) > 0 or len(obj["info_stealer"]) > 0}.values())
        json.dump(unique_objects, file_data, indent=4)
