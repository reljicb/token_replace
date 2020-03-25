import re
import string
from reference_supplier import ReferenceSupplier


class RawToken:
    def __init__(self, (key, value), reference_supplier=ReferenceSupplier()):
        self.set_tokens_dict = dict()

        # sanitize key and value
        self.key = key.strip()
        self.value = value

        self.replaced_flag = False
        self.circular_dependency_flag = None

        # extract references to other tokens in value
        raw_refs = re.compile("(?:{{[^}]+}}|~{[^}]+}~|%{[^}]+}%)").findall(self.value)

        # populate reference dict
        self.references_dict = dict()
        for ref_with_delims in raw_refs:
            # sanitize references by removing delimiting chars
            ref_name = re.sub("({{|}}|~{|}~|%{|}%)", "", ref_with_delims)
            ref = reference_supplier.get_reference(ref_name, self)
            if ref.name not in self.references_dict:
                self.references_dict[ref.name] = ReferenceWrapper()
            self.references_dict[ref.name].ref = ref
            self.references_dict[ref.name].refs_with_delims.append(ref_with_delims)

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

    def get_replaced_value(self):
        ret = self.value
        for (ref_name, ref_wrapper) in self.references_dict.items():
            if ref_name not in self.set_tokens_dict:
                continue
            val = self.set_tokens_dict[ref_name].get_replaced_value()
            for ref_with_delims in ref_wrapper.refs_with_delims:
                ret = string.replace(ret, ref_with_delims, val)
        return ret

    def __str__(self):
        return self.key + "=" + self.get_replaced_value()

    def __repr__(self):
        return str(self)


class ReferenceWrapper:

    def __init__(self):
        self.ref = None
        self.refs_with_delims = []
