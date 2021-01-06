import argparse
import os
import sys

from loguru import logger

from httprunner import __description__, __version__
from httprunner.api import HttpRunner
from httprunner.report import gen_html_report
from httprunner.utils import create_scaffold


def main():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)  # < - - - 初始化一个分析器
    parser.add_argument(
        '-V', '--version', dest='version', action='store_true',
        help="show version")
    parser.add_argument(
        'testfile_paths', nargs='*',  # < - - - * 的意思是传0-无数个
        help="Specify api/testcase/testsuite file paths to run.")
    parser.add_argument(
        '--log-level', default='INFO',
        help="Specify logging level, default is INFO.")
    parser.add_argument(
        '--log-file',
        help="Write logs to specified file path.")
    parser.add_argument(
        '--dot-env-path',
        help="Specify .env file path, which is useful for keeping sensitive data.")
    parser.add_argument(
        '--report-template',
        help="Specify report template path.")
    parser.add_argument(
        '--report-dir',
        help="Specify report save directory.")
    parser.add_argument(
        '--report-file',
        help="Specify report file path, this has higher priority than specifying report dir.")
    parser.add_argument(
        '--save-tests', action='store_true', default=False,
        help="Save loaded/parsed/vars_out/summary json data to JSON files.")
    parser.add_argument(
        '--failfast', action='store_true', default=False,
        help="Stop the test run on the first error or failure.")
    parser.add_argument(
        '--startproject',
        help="Specify new project name.")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        # no argument passed
        parser.print_help()
        sys.exit(0)

    if args.version:
        print(f"{__version__}")
        sys.exit(0)

    project_name = args.startproject
    if project_name:
        create_scaffold(project_name)
        sys.exit(0)

    runner = HttpRunner(  # <--- 创建一个HttpRunner实例
        failfast=args.failfast,  # <--- 失败后停止运行
        save_tests=args.save_tests,
        log_level=args.log_level,
        log_file=args.log_file
    )

    err_code = 0
    try:
        for path in args.testfile_paths:
            summary = runner.run(path, dot_env_path=args.dot_env_path)  # <--- 执行测试文件，运行测试结果
            report_dir = args.report_dir or os.path.join(os.getcwd(), "reports")  # <--- 获取report路径
            gen_html_report(
                summary,
                report_template=args.report_template,
                report_dir=report_dir,
                report_file=args.report_file
            )
            err_code |= (0 if summary and summary["success"] else 1)    # <--- == err_code | summary的结果，只要有一个结果为1，就为1
    except Exception as ex:  # <--- == 捕获异常并打印
        logger.error(f"!!!!!!!!!! exception stage: {runner.exception_stage} !!!!!!!!!!\n{str(ex)}")
        err_code = 1

    sys.exit(err_code)  # <--- 0正常退出 1有错误退出


if __name__ == '__main__':
    main()
