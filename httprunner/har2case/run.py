from httprunner.har2case import core


def run_har2case():
    """
    har to testfile
    :return: null
    """
    # a = core.HarParser("testcase/gmc-test.cfuture.shop.har")
    a = core.HarParser("testcase/gmc-test.cfuture.shop.har", change=True)

    a.gen_testcase(file_type="YML")


if __name__ == '__main__':
    run_har2case()