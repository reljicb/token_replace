from utils.raw_token import RawToken

SUPPORTED_DELIMITERS = [("{{", "}}")]


def should_replace_token():
    rt_key1 = RawToken(("key1", "value {{key2}} value {{key3}} value {{key4}} value"), SUPPORTED_DELIMITERS)
    rt_key2 = RawToken(("key2", "value2"), SUPPORTED_DELIMITERS)
    rt_key3 = RawToken(("key3", "value3"), SUPPORTED_DELIMITERS)
    rt_key1.set_token(rt_key3)
    rt_key1.set_token(rt_key2)

    returned = str(rt_key1)
    print "returned replaced token: %s" % returned

    expected = "key1=value value2 value value3 value {{key4}} value"
    assert returned == expected, "returned %s different from expected %s" % (returned, expected)


def run_all_tests():
    should_replace_token()


if __name__ == "__main__":
    run_all_tests()
