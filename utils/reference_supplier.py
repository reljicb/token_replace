class ReferenceSupplier:

    def __init__(self):
        self.references = {}

    def get_reference(self, name, for_raw_token):
        if name not in self.references:
            self.references[name] = Reference(name)

        self.references[name].linked_raw_tokens_list.append(for_raw_token)
        return self.references[name]

    def __str__(self):
        return self.references

    def __repr__(self):
        return str(self)


class Reference:

    def __init__(self, name):
        self.name = name
        self.linked_raw_tokens_list = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
