import utils.strings as str


def should_split_file_to_list():
    input_file = """
    key1=val1
    key2 = val2  
    key3=  val3.1  \\
val3.2\\ 
  val3.3
    key4 =val4  
    key5
    key6=val6
    """

    returned = str.convert_string_to_key_value_tuples(input_file)
    print "returned converted file to tuples: %s" % returned

    expected = [("key1", "val1"), ("key2", " val2"), ("key3", "  val3.1\nval3.2\n  val3.3"),
                ("key4", "val4"), ("key5", ""), ("key6", "val6")]
    assert returned == expected, "returned %s different from expected %s" % (returned, expected)


def should_merge_multiline_props_to_single_line():
    input_file = \
        """
key1=val1
key2 = val2\\   
  val3 \\  
 val5  
key4 =val4  
"""

    returned = str.merge_multiline_properties(input_file)
    print "returned merged multiline property file to single line: %s" % returned

    expected = \
        """
key1=val1
key2 = val2<REPLACE-LF>  val3<REPLACE-LF> val5  
key4 =val4  
"""
    assert returned == expected, "returned %s different from expected %s" % (returned, expected)


def run_all_tests():
    should_split_file_to_list()
    should_merge_multiline_props_to_single_line()


if __name__ == "__main__":
    run_all_tests()
