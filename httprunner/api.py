import os
import sys
import unittest
import json
from loguru import logger
import copy
from httprunner import (__version__, exceptions, loader, parser,
                        report, runner, utils)


class HttpRunner(object):
    """ Developer Interface: Main Interface
        Usage:

            from httprunner.api import HttpRunner
            runner = HttpRunner(
                failfast=True,
                save_tests=True,
                log_level="INFO",
                log_file="test.log"
            )
            summary = runner.run(path_or_tests)

    """

    def __init__(self, failfast=False, save_tests=False, log_level="WARNING", log_file=None):
        """ initialize HttpRunner.

        Args:
            failfast (bool): stop the test run on the first error or failure.
            save_tests (bool): save loaded/parsed tests to JSON file.
            log_level (str): logging level.
            log_file (str): log file path.

        """
        self.exception_stage = "initialize HttpRunner()"  # < - - - 这个参数的主要作用是设置一下测试运行的阶段
        kwargs = {
            "failfast": failfast,  # < - - - unittest失败不跳过策略
            "resultclass": report.HtmlTestResult  # < - - - 定制测试结果
        }

        logger.remove()
        log_level = log_level.upper()
        logger.add(sys.stdout, level=log_level)
        if log_file:
            logger.add(log_file, level=log_level)

        self.unittest_runner = unittest.TextTestRunner(**kwargs)  # < - - - 创建unittest TextTestRunner实例
        self.test_loader = unittest.TestLoader()  # < - - - unittest 查找测试类的方法
        self.save_tests = save_tests
        self._summary = None
        self.test_path = None
        self.tag = None


    def _add_tests(self, testcases):
        """ initialize testcase with Runner() and add to test suite.

        Args:
            testcases (list): testcases list.

        Returns:
            unittest.TestSuite()

        """
        def _add_test(test_runner, test_dict):
            """ add test to testcase.
            """
            def test(self):
                try:
                    test_runner.run_test(test_dict)
                except exceptions.MyBaseFailure as ex:
                    self.fail(str(ex))
                finally:
                    self.meta_datas = test_runner.meta_datas

            if "config" in test_dict:
                # run nested testcase
                test.__doc__ = test_dict["config"].get("name")
                variables = test_dict["config"].get("variables", {})
            else:
                # run api test
                test.__doc__ = test_dict.get("name")
                variables = test_dict.get("variables", {})

            if isinstance(test.__doc__, parser.LazyString):
                try:
                    parsed_variables = parser.parse_variables_mapping(variables)
                    test.__doc__ = parser.parse_lazy_data(
                        test.__doc__, parsed_variables
                    )
                except exceptions.VariableNotFound:
                    test.__doc__ = str(test.__doc__)

            return test


        test_suite = unittest.TestSuite()
        new_testcases = []
        if self.tag:  # < - - - 传參有tag的时候，只选择包含tag的testcase
            for testcase in testcases:
                config = testcase.get("config", {})
                tag = config.get("tag", [])
                if self.tag in tag:
                    new_testcases.append(testcase)
            testcases = new_testcases

        for testcase in testcases:
            config = testcase.get("config", {})
            tests = testcase.get("teststeps", [])
            for tests_sub in tests[::-1]:  # < - - - 倒序读取
                index = tests.index(tests_sub)
                if "teststeps" in tests_sub and "config" in tests_sub:
                    tests_sub.get("config", {}).update(config)
                    config = tests_sub.get("config", {})
                    for index_subs, test_dict_sub in enumerate(tests_sub.get("teststeps")):
                        index_subs += 1
                        tests.insert(index+index_subs, test_dict_sub)
                    tests.remove(tests_sub)



            test_runner = runner.Runner(config)
            TestSequense = type('TestSequense', (unittest.TestCase,), {})

            for index, test_dict in enumerate(tests):  # < - - - 获取重试次数，默认1次
                times = test_dict.get("times", 1)
                try:
                    times = int(times)
                except ValueError:
                    raise exceptions.ParamsError(
                        f"times should be digit, given: {times}")

                for times_index in range(times):
                    # suppose one testcase should not have more than 9999 steps,
                    # and one step should not run more than 999 times.
                    test_method_name = 'test_{:04}_{:03}'.format(index, times_index)
                    test_dict['name'] = test_dict['name'] + ':'+ test_method_name

                    test_method = _add_test(test_runner, test_dict)

                    setattr(TestSequense, test_method_name, test_method)

            loaded_testcase = self.test_loader.loadTestsFromTestCase(TestSequense)
            setattr(loaded_testcase, "config", config)
            setattr(loaded_testcase, "teststeps", tests)
            setattr(loaded_testcase, "runner", test_runner)
            test_suite.addTest(loaded_testcase)
        return test_suite

    def _run_suite(self, test_suite):
        """ run tests in test_suite

        Args:
            test_suite: unittest.TestSuite()

        Returns:
            list: tests_results

        """
        tests_results = []

        for index, testcase in enumerate(test_suite):
            log_handler = None
            if self.save_tests:
                logs_file_abs_path = utils.prepare_log_file_abs_path(
                    self.test_path, f"testcase_{index+1}.log"
                )
                log_handler = logger.add(logs_file_abs_path, level="DEBUG")

            testcase_name = testcase.config.get("name")

            logger.info(f"Start to run testcase: {testcase_name}")
            result = self.unittest_runner.run(testcase)  # < - - - 执行testcase

            if result.wasSuccessful():
                tests_results.append((testcase, result))
            else:
                tests_results.insert(0, (testcase, result))

            if self.save_tests and log_handler:
                logger.remove(log_handler)
        return tests_results

    def _aggregate(self, tests_results):
        """ aggregate results

        Args:
            tests_results (list): list of (testcase, result)

        """
        summary = {
            "success": True,
            "stat": {
                "testcases": {
                    "total": len(tests_results),
                    "success": 0,
                    "fail": 0
                },
                "teststeps": {}
            },
            "time": {},
            "platform": report.get_platform(),
            "details": []
        }

        for index, tests_result in enumerate(tests_results):
            testcase, result = tests_result
            testcase_summary = report.get_summary(result)

            if testcase_summary["success"]:
                summary["stat"]["testcases"]["success"] += 1
            else:
                summary["stat"]["testcases"]["fail"] += 1

            summary["success"] &= testcase_summary["success"]
            testcase_summary["name"] = testcase.config.get("name")
            testcase_summary["in_out"] = utils.get_testcase_io(testcase)

            report.aggregate_stat(summary["stat"]["teststeps"], testcase_summary["stat"])
            report.aggregate_stat(summary["time"], testcase_summary["time"])
            if self.save_tests:
                logs_file_abs_path = utils.prepare_log_file_abs_path(
                    self.test_path, f"testcase_{index+1}.log"
                )
                testcase_summary["log"] = logs_file_abs_path

            # testcase_summary["HRUN-Request-ID"] = testcase.runner.hrun_request_id
            summary["details"].append(testcase_summary)
        summary['details'] = self.change_summary(summary['details'])  # < - - - summary['details']和summary['stat']['teststeps']是笔者为了将重试次数合并添加的
        summary['stat']['teststeps'] = self.change_steps(summary['details'])
        # Aone实验室展示测试结果（设置卡点时用）
        # utils.print_aone_laboratory(summary)
        return summary

    def change_summary(self, summary_details):
        for i in summary_details:
            stat = {
                'total': 0,
                'failure': 0,
                'error': 0,
                'skipped': 0,
                'expectedFailure': 0,
                'unexpectedSuccess': 0,
                'success': 0
            }
            if len(i) > 1:
                for j, k in enumerate(i['records']):
                    for s in i['records'][j + 1:]:
                        if s['name'].split(":")[1] == k['name'].split(":")[1]:
                            i['records'].pop(j)
                        else:
                            break
            for m in i['records']:
                stat[m['status']] += 1
                m['name'] = m['name'].split(":")
                times = len(m['name']) - 2
                if times > 1:
                    m['name'] = f"{m['name'][0]}(第{times}次重试)"
                else:
                    m['name'] = m['name'][0]

            i['stat']['total'] = sum(stat.values())
            i['stat']['failures'] = stat['failure']
            i['stat']['skipped'] = stat['skipped']
            i['stat']['errors'] = stat['error']
            i['stat']['expectedFailures'] = stat['expectedFailure']
            i['stat']['unexpectedSuccesses'] = stat['unexpectedSuccess']
            i['stat']['successes'] = stat['success']

        return summary_details

    def change_steps(self, summary_steps):
        result = {
                'total': 0,
                'failures': 0,
                'errors': 0,
                'skipped': 0,
                'expectedFailures': 0,
                'unexpectedSuccesses': 0,
                'successes': 0}
        for i in summary_steps:
            for j, k in i['stat'].items():
                result[j] += k
        return result


    def run_tests(self, tests_mapping):
        """ run testcase/testsuite data
        """
        self.test_path = tests_mapping.get("project_mapping", {}).get("test_path", "")
        if self.save_tests:
            utils.dump_json_file(
                tests_mapping,
                utils.prepare_log_file_abs_path(self.test_path, "loaded.json")
            )

        # parse tests
        self.exception_stage = "parse tests"
        parsed_testcases = parser.parse_tests(tests_mapping)  # < - - - 解析testcases
        parse_failed_testfiles = parser.get_parse_failed_testfiles()
        if parse_failed_testfiles:
            logger.warning("parse failures occurred ...")
            utils.dump_json_file(
                parse_failed_testfiles,
                utils.prepare_log_file_abs_path(self.test_path, "parse_failed.json")
            )

        if len(parsed_testcases) == 0:
            logger.error("failed to parse all cases, abort.")
            raise exceptions.ParseTestsFailure

        if self.save_tests:
            utils.dump_json_file(
                parsed_testcases,
                utils.prepare_log_file_abs_path(self.test_path, "parsed.json")
            )

        # add tests to test suite
        self.exception_stage = "add tests to test suite"
        test_suite = self._add_tests(parsed_testcases)  # < - - - 创建test_suite
        # run test suite
        self.exception_stage = "run test suite"
        results = self._run_suite(test_suite)  # < - - - 执行test_suite

        # aggregate results
        self.exception_stage = "aggregate results"
        self._summary = self._aggregate(results)  # < - - - 合并测试结果，如果想要修改测试报告中的结果可以在这里修改

        # generate html report
        self.exception_stage = "generate html report"
        report.stringify_summary(self._summary) # < - - - 生产测试报告

        if self.save_tests:
            utils.dump_json_file(
                self._summary,
                utils.prepare_log_file_abs_path(self.test_path, "summary.json")
            )
            # save variables and export data
            vars_out = self.get_vars_out()
            utils.dump_json_file(
                vars_out,
                utils.prepare_log_file_abs_path(self.test_path, "io.json")
            )

        return self._summary

    def get_vars_out(self):
        """ get variables and output
        Returns:
            list: list of variables and output.
                if tests are parameterized, list items are corresponded to parameters.

                [
                    {
                        "in": {
                            "user1": "leo"
                        },
                        "out": {
                            "out1": "out_value_1"
                        }
                    },
                    {...}
                ]

            None: returns None if tests not started or finished or corrupted.

        """
        if not self._summary:
            return None

        return [
            summary["in_out"]
            for summary in self._summary["details"]
        ]

    def run_path(self, path, dot_env_path=None, mapping=None):
        """ run testcase/testsuite file or folder.

        Args:
            path (str): testcase/testsuite file/foler path.
            dot_env_path (str): specified .env file path.
            mapping (dict): if mapping is specified, it will override variables in config block.

        Returns:
            dict: result summary

        """
        # load tests
        self.exception_stage = "load tests"
        tests_mapping = loader.load_cases(path, dot_env_path)  # < - - - 初始化测试集

        if mapping:
            tests_mapping["project_mapping"]["variables"] = mapping

        return self.run_tests(tests_mapping)

    def run(self, path_or_tests, dot_env_path=None, mapping=None, tag=None):
        """ main interface.

        Args:
            path_or_tests:
                str: testcase/testsuite file/foler path
                dict: valid testcase/testsuite data
            dot_env_path (str): specified .env file path.
            mapping (dict): if mapping is specified, it will override variables in config block.
            tag: select testcase/testsuite use tag
        Returns:
            dict: result summary

        """
        # logger.info(f"HttpRunner version: {__version__}")
        logger.info(f"Thanos2.0")
        self.tag = tag
        if loader.is_test_path(path_or_tests):  # < - - - 如果是路径，执行run_path方法
            return self.run_path(path_or_tests, dot_env_path, mapping)
        elif loader.is_test_content(path_or_tests):
            project_working_directory = path_or_tests.get("project_mapping", {}).get("PWD", os.getcwd())
            loader.init_pwd(project_working_directory)
            return self.run_tests(path_or_tests)  # < - - - 如果是文件，直接执行run_tests
        else:
            raise exceptions.ParamsError(f"Invalid testcase path or testcases: {path_or_tests}")
