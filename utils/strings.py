import re

# TODO: implement multiline values


def convert_string_to_key_value_tuples(input_file):
    lines = input_file.split("\n")
    key_values = [sanitize_tuple(tuple(re.split("=", line.strip(), 1))) for line in lines if line.strip()]
    return [key_value for key_value in key_values if len(key_value) > 1]


def sanitize_tuple(tuple_line):
    (k, v) = tuple_line
    return tuple([k.strip(), v])

