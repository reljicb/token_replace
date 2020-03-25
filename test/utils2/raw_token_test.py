from utils.raw_token import RawToken
from utils.reference_supplier import ReferenceSupplier


def should_replace_token():
    rt_key1 = RawToken(("key1", "value {{key2}} value {{key3}} value {{key4}} value"))
    rt_key2 = RawToken(("key2", "value2"))
    rt_key3 = RawToken(("key3", "value3"))
    rt_key1.set_token(rt_key3)
    rt_key1.set_token(rt_key2)

    returned = str(rt_key1)
    print "returned replaced token: %s" % returned

    expected = "key1=value value2 value value3 value {{key4}} value"
    assert returned == expected, "returned %s different from expected %s" % (returned, expected)


def should_link_all_references():
    reference_supplier = ReferenceSupplier()
    RawToken(("key1", "value {{key2}} value ~{key2}~ value %{key2}% value {{key3}} value"), reference_supplier)

    returned = set(reference_supplier.references.keys())
    print "returned references: %s" % returned

    expected = set(["key2", "key3"])
    assert returned == expected, "returned %s different from expected %s" % (returned, expected)


def run_all_tests():
    should_replace_token()
    should_link_all_references()


if __name__ == "__main__":
    run_all_tests()
