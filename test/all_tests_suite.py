import replace_test
import utils2.strings_test as strings_test
import utils2.raw_token_test as raw_token_test


def run_all_tests():
    replace_test.run_all_tests()
    strings_test.run_all_tests()
    raw_token_test.run_all_tests()


if __name__ == "__main__":
    run_all_tests()
