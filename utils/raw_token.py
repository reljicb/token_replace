import re
import string


class RawToken:
    def __init__(self, (key, value), delimiters):
        self.set_tokens_dict = dict()

        # sanitize key and value
        self.key = key.strip()
        self.value = value

        self.replaced_flag = False
        self.circular_dependency_flag = None

        # extract references to other tokens in value
        raw_refs = re.compile(build_regex_patter(delimiters)).findall(self.value)

        # populate reference dict
        self.references_dict = dict()
        for ref_with_delims in raw_refs:
            # sanitize references by removing delimiting chars
            ref_name = re.sub("({{|}}|~{|}~|%{|}%)", "", ref_with_delims)
            if ref_name not in self.references_dict:
                self.references_dict[ref_name] = []
            self.references_dict[ref_name].append(ref_with_delims)

    def set_token(self, raw_token):
        if not hasattr(raw_token, "key"):
            return False

        if raw_token.key not in self.references_dict:
            return False

        self.set_tokens_dict[raw_token.key] = raw_token

        return True

    def set_replaced_flag(self):
        self.replaced_flag = True

    def set_circular_dependency_flag(self, msg):
        self.circular_dependency_flag = msg

    def get_replaced_value(self, call_stack=[]):
        ret = self.value

        if self.key in call_stack:
            return False, "ERROR: CIRCULAR_DEPENDENCY: " + " > ".join(call_stack + [self.key])

        for (ref_name, refs_with_delims) in self.references_dict.items():
            if ref_name not in self.set_tokens_dict:
                continue
            is_status_ok, value = self.set_tokens_dict[ref_name].get_replaced_value(call_stack + [self.key])
            if not is_status_ok:
                return is_status_ok, value

            for ref_with_delims in refs_with_delims:
                ret = string.replace(ret, ref_with_delims, value)

        return True, ret

    def __str__(self):
        is_status_ok, val = self.get_replaced_value()
        return self.key + "=" + val

    def __repr__(self):
        return str(self)


def build_regex_patter(delimiters):
    ret = "(?:%s)" % "|".join(["%(left_del)s[^%(right_del_first_char)s]+%(right_del)s" % {
        "left_del": left_del,
        "right_del_first_char": right_del[:1],
        "right_del": right_del
    } for (left_del, right_del) in delimiters])
    return ret
