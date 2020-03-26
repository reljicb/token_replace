import re

TEMP_LF_DELIMITER = "<REPLACE-LF>"


def merge_multiline_properties(input_file):
    lines = re.split("\s*\\\\\s*\n", input_file, re.MULTILINE)
    return TEMP_LF_DELIMITER.join([line for line in lines if line.strip()])


def convert_string_to_key_value_tuples(input_file):
    single_input_file = merge_multiline_properties(input_file)

    lines = single_input_file.split("\n")
    key_values = [sanitize_tuple(tuple(re.split("=", line.strip().replace(TEMP_LF_DELIMITER, "\n"), 1)))
                  for line in lines
                  if _is_property_line(line) ]
    return [key_value for key_value in key_values if len(key_value) > 1]


# ignore:
#  1. empty lines,
#  2. commented lines (with #),
#  3. lines which do not contain unescaped equal sign
def _is_property_line(line):
    line = line.strip()

    if not line \
            or re.match("\s*[\#].*", line):
        return False

    if re.match("[^=]*[^\\\\]=.*", line):
        return True

    return False


def sanitize_tuple(tup):
    (k, v) = (tup[0], tup[1]) if len(tup) > 1 else (tup[0], "")
    return tuple([k.strip(), v])

