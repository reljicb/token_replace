from utils.raw_token import RawToken
from utils.reference_supplier import ReferenceSupplier
import utils.strings as u_str

# TODO: define all tokens here, and split and use them later

FILE_1 = """
    k1=(k1 v1)
    k2=(k2 v3: {{k3}})  
    """

FILE_2 = """
    k3=(k3 k1: {{k1}})
    """


def main():
    reference_supplier = ReferenceSupplier()
    tokens_dict = get_merged_tokens_dict([FILE_1, FILE_2], reference_supplier)

    for (token_name, token) in tokens_dict.items():

        for (ref_name, reference) in token.references_dict.items():
            if ref_name in tokens_dict:
                ref_token = tokens_dict[ref_name]
                token.set_token(ref_token)

    for (token_name, token) in tokens_dict.items():
        print token


def get_merged_tokens_dict(input_files, reference_supplier):
    def convert_to_raw_token_list(file):
        ret = [RawToken((key, value), reference_supplier) for (key, value) in u_str.convert_string_to_key_value_tuples(file)]
        return ret
    all_raw_tokens = []
    for input_file in input_files:
        all_raw_tokens += [t for t in convert_to_raw_token_list(input_file)]

    return {t.key: t for t in all_raw_tokens}


if __name__ == "__main__":
    main()
