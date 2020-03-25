import utils.strings as str


def should_split_file_to_list():
    file_1 = """
    key1=val1
    key2 = val2  
    key3=  val3  
    key4 =val4  
    """

    returned = str.convert_string_to_key_value_tuples(file_1)
    print "returned converted file to tuples: %s" % returned

    expected = [("key1", "val1"), ("key2", " val2"), ("key3", "  val3"), ("key4", "val4")]
    assert returned == expected, "returned %s different from expected %s" % (returned, expected)


def run_all_tests():
    should_split_file_to_list()


if __name__ == "__main__":
    run_all_tests()
