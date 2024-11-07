import utils.logs


class DataManager:
    def __init__(self):
        self.reset()
        self.index = {}

    def push(self, key, attribute, value):
        # Update manager attributes
        current_value = getattr(self, attribute)
        if isinstance(value, list):
            current_value.extend(value)
            setattr(self, attribute, current_value)
        else:
            setattr(self, attribute, value)

        # Update statistics
        if not isinstance(value, list):
            return

        if key not in self.index:
            self.index[key] = {}
        if attribute not in self.index[key]:
            self.index[key][attribute] = []

        current_value = self.index[key][attribute]
        current_value.extend(value)
        self.index[key][attribute] = current_value

    def pop(self):
        passwords = list(set(self.passwords))
        new_emails = [e.lower() for e in set(self.new_emails)]
        info_stealer = self.info_stealer
        breaches = self.breaches
        is_password_exposed = self.is_password_exposed
        hashes = list(set(self.hashes))
        ips = list(set(self.ips))
        self.reset()
        return passwords, new_emails, info_stealer, breaches, is_password_exposed, hashes, ips


    def stats(self):
        utils.logs.notice("========= Stats =========")

        for key, attributes in self.index.items():
            for attribute, value in attributes.items():
                _s = value[0]
                if isinstance(_s, str):
                    value = list(set(value))
                utils.logs.notice(f'[{key:20} --> {attribute:10}] Found {len(value)} unique values.')

        for exclusive_attribute in ['passwords', 'hashes']:
            for key, attributes in self.index.items():
                if exclusive_attribute not in attributes:
                    continue
                passwords = list(set(attributes[exclusive_attribute]))
                all_passwords = []
                for _key, _attributes in self.index.items():
                    if key == _key or exclusive_attribute not in _attributes:
                        continue
                    all_passwords.extend(_attributes[exclusive_attribute])

                all_passwords = list(set(all_passwords))
                unique_passwords = [p for p in passwords if p not in all_passwords]

                utils.logs.notice(f'[{key:20} --> {exclusive_attribute:10}] Found {len(unique_passwords)} exclusive {exclusive_attribute}.')

    def reset(self):
        self.passwords = []
        self.new_emails = []
        self.info_stealer = []
        self.breaches = []
        self.is_password_exposed = False
        self.hashes = []
        self.ips = []
