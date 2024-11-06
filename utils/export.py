import utils.logs

leakcheck_message = False


def compute_entry(entry, result, added_emails):
    global leakcheck_message
    passwords = []
    hashes = []
    emails = entry['emails']
    info_stealer = []
    breaches = []
    is_password_exposed = False
    for email in entry['emails']:
        if email in result:
            if 'passwords' in result[email]:
                passwords.extend(result[email]['passwords'])
            if 'hashes' in result[email]:
                hashes.extend(result[email]['hashes'])
            if 'info_stealer' in result[email]:
                info_stealer.extend(result[email]['info_stealer'])
            if 'breaches' in result[email]:
                is_password_exposed = result[email]['breaches']['password_leaked']
                breaches.extend(result[email]['breaches']['list'])
        if email in added_emails:
            emails.extend(added_emails[email])

    entry['passwords'] = list(set(passwords))
    entry['hashes'] = list(set(hashes))
    entry['emails'] = list(set(emails))
    entry['info_stealer'] = info_stealer
    entry['breaches'] = breaches

    if is_password_exposed and len(passwords) == 0:
        if not leakcheck_message:
            utils.logs.info(f"You can view additional censored passwords (for free) at "
                            f"'https://leakcheck.io' for at least one email.")
            leakcheck_message = True
        utils.logs.warning(f"Password was exposed in breaches, not none were found for: {entry['id']} ({entry['emails']})")

    return entry
