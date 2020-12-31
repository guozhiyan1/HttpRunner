from httprunner import har2case as core


def run_har2case():
    """
    har to testfile
    :return: null
    """
    # a = core.HarParser("testcase/new.har")
    a = core.HarParser("testcase/new.har", change=True)

    a.gen_testcase(file_type="YML")


if __name__ == '__main__':
    run_har2case()