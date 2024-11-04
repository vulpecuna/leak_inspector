import argparse
import json
import os


class ProgramArgs:
    def __init__(self, args):
        emails = []

        for input_file in args.scrapped_data:
            with open(input_file, 'r') as file:
                data = json.load(file)
            for entry in data['emails']:
                for email in entry['emails']:
                    emails.append((email, email))

        self.emails = list(set(emails))
        self.sources = args.scrapped_data


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

    # Parse the arguments
    raw_args = parser.parse_args()
    return ProgramArgs(raw_args)
