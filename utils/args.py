import argparse
import json
import os


class ProgramArgs:
    def __init__(self, args):
        emails = []

        for input_file in args.scrapped_data:
            with open(input_file, 'r') as file:
                entries = json.load(file)
            for entry in entries:
                for email in entry['emails']:
                    emails.append((email, email))

        self.emails = list(set(emails))
        self.sources = args.scrapped_data
        self.domain = args.domain

        self.proxynova_enabled = args.proxynova_enabled
        self.hudson_enabled = args.hudson_enabled
        self.leakcheck_enabled = args.leakcheck_enabled
        self.snusbase_api_key = args.snusbase_api_key


def _file_exists(file_path):
    """Check if the file exists."""
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"The file {file_path} does not exist.")
    return file_path


def parse():
    parser = argparse.ArgumentParser(description="Leak Inspector")
    parser.add_argument(
        'scrapped_data',
        nargs='+',
        type=_file_exists,
        help='Linkedin OSINT tool output file.'
    )
    parser.add_argument(
        '-d', '--domain',
        type=str,
        default=None,
        help='Domain to use for domain search (if enabled APIs support it).'
    )

    parser.add_argument('-a', '--all', dest='all_enabled', action='store_true', help='Enable every unauthenticated API for uncached results (default: disabled)')
    parser.add_argument('--hudson', dest='hudson_enabled', action='store_true', help='Enable HudsonRocks API for uncached results (default: disabled)')
    parser.add_argument('--proxynova', dest='proxynova_enabled', action='store_true', help='Enable ProxyNova API for uncached results (default: disabled)')
    parser.add_argument('--leakcheck', dest='leakcheck_enabled', action='store_true', help='Enable LeakCheck APIs for uncached results (default: disabled)')
    parser.add_argument('--snusbase', type=str, dest='snusbase_api_key', default=None, help='Use your API key to access Snusbase APIs for uncached results (default: disabled)')

    # Parse the arguments
    raw_args = parser.parse_args()

    if raw_args.all_enabled:
        setattr(raw_args, 'hudson_enabled', True)
        setattr(raw_args, 'proxynova_enabled', True)
        setattr(raw_args, 'leakcheck_enabled', True)

    is_enabled = raw_args.proxynova_enabled or raw_args.hudson_enabled or raw_args.leakcheck_enable
    is_enabled = is_enabled or raw_args.snusbase_api_key
    if not is_enabled:
        parser.error(f"At least one API must be enabled. Please specify which APIs to use.")

    return ProgramArgs(raw_args)
