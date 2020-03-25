import re

TEMP_LF_DELIMITER = "<REPLACE-LF>"


def merge_multiline_properties(input_file):
    lines = re.split("\s*\\\\\s*\n", input_file, re.MULTILINE)
    return TEMP_LF_DELIMITER.join([line for line in lines if line.strip()])


def convert_string_to_key_value_tuples(input_file):
    single_input_file = merge_multiline_properties(input_file)

    lines = single_input_file.split("\n")
    key_values = [sanitize_tuple(tuple(re.split("=", line.strip().replace(TEMP_LF_DELIMITER, "\n"), 1))) for line in lines if line.strip()]
    return [key_value for key_value in key_values if len(key_value) > 1]


def sanitize_tuple((k, v)):
    return tuple([k.strip(), v])

