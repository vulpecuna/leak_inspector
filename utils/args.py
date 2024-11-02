import argparse
import json
import os


class ProgramArgs:
    def __init__(self, args):
        with open(args.input_file, 'r') as file:
            data = json.load(file)
            emails = []
            for entry in data['emails']:
                for email in entry['emails']:
                    emails.append((email, email))

            self.emails = list(set(emails))

        self.input_file = args.input_file


def _file_exists(file_path):
    """Check if the file exists."""
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"The file {file_path} does not exist.")
    return file_path


def parse():
    parser = argparse.ArgumentParser(description="Leak Inspector")
    input_options = parser.add_mutually_exclusive_group(required=True)
    input_options.add_argument(
        '-f',
        metavar='input.json',
        dest='input_file',
        type=_file_exists,
        help='Linkedin OSINT tool output file.'
    )

    # Parse the arguments
    raw_args = parser.parse_args()
    return ProgramArgs(raw_args)
