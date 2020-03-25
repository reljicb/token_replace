import replace


def should_take_latest_token_value():
    file_1 = """
        NAME1=  Some value
        NAME2 =  Value2: {{NAME1}}  
        """

    file_2 = """
        NAME1=Some value from file 2
        NAME3=Value2: {{NAME2}}
        """

    returned = replace.get_merged_tokens_dict([file_1, file_2])
    returned = {it[0]: it[1].value for it in returned.items()}

    expected = {"NAME1": "Some value from file 2",
                "NAME2": "  Value2: {{NAME1}}",
                "NAME3": "Value2: {{NAME2}}"}

    print "returned merged token dict: %s" % returned

    assert returned == expected, "returned %s different from expected %s" % (returned, expected)


def run_all_tests():
    should_take_latest_token_value()


if __name__ == "__main__":
    run_all_tests()
