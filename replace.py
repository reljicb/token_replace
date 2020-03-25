from utils.raw_token import RawToken
import utils.strings as u_str

DELIMITERS = [("{{", "}}"), ("~{", "}~"), ("%{", "}%")]

FILE_1 = """
    k1=(v1 p2: {{k2}})
    k2=(v2 p3: ~{k3}~)
    k4=(v4 p5: %{k5}%)
    k7=(v7 p6: ~{k6}~)  
    """

FILE_2 = """
    k3=(v3 p1: {{k1}})
    k5=v5
    k6=(v6 multiline \\
text\\  
 end
    """


def main():
    tokens_dict = get_merged_tokens_dict([FILE_1, FILE_2])

    for (token_name, token) in tokens_dict.items():

        for (ref_name, reference) in token.references_dict.items():
            if ref_name in tokens_dict:
                ref_token = tokens_dict[ref_name]
                token.set_token(ref_token)

    for (token_name, token) in tokens_dict.items():
        print token


def get_merged_tokens_dict(input_files):
    def convert_to_raw_token_list(file):
        ret = [RawToken((key, value), DELIMITERS) for (key, value) in u_str.convert_string_to_key_value_tuples(file)]
        return ret
    all_raw_tokens = []
    for input_file in input_files:
        all_raw_tokens += [t for t in convert_to_raw_token_list(input_file)]

    return {t.key: t for t in all_raw_tokens}


if __name__ == "__main__":
    main()
