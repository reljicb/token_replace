from utils.raw_token import RawToken
import utils.strings as u_str
from argparse import ArgumentParser


def main():
    args = get_arguments()

    all_files = [read_file_to_string(file_path) for file_path in args.property_file_csv_paths.split(",")]
    supported_delims = get_delimiters_from_csv(args.supported_delimiters_csv)

    tokens_dict = get_merged_tokens_dict(all_files, supported_delims)

    for (token_name, token) in tokens_dict.items():

        for (ref_name, reference) in token.references_dict.items():
            if ref_name in tokens_dict:
                ref_token = tokens_dict[ref_name]
                token.set_token(ref_token)

    for (token_name, token) in tokens_dict.items():
        print token


def get_merged_tokens_dict(input_files, supported_delims):
    def convert_to_raw_token_list(file):
        ret = [RawToken((key, value), supported_delims) for (key, value) in u_str.convert_string_to_key_value_tuples(file)]
        return ret
    all_raw_tokens = []
    for input_file in input_files:
        all_raw_tokens += [t for t in convert_to_raw_token_list(input_file)]

    return {t.key: t for t in all_raw_tokens}


def read_file_to_string(file_path):
    with open(file_path.strip(), 'r') as f:
        return f.read()


def get_delimiters_from_csv(supported_delimiters_csv):
    def get_tupple_split_in_middle(delim):
        mid_str = int(round(len(delim)/2, 0))
        return delim[:mid_str], delim[mid_str:]

    return [get_tupple_split_in_middle(delim.strip()) for delim in supported_delimiters_csv.split(",")]


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("-d", "--supported-delimiters-csv",
                        help="Comma separated list of supported token delimiters" +
                             " (pairs, left+right, for example: \"{{}},~{}~\")")
    parser.add_argument("-f", "--property-file-csv-paths",
                        help="Comma separated list of file paths containing key=value pair properties.")

    return parser.parse_args()


if __name__ == "__main__":
    main()
