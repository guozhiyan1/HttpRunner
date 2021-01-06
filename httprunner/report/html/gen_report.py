import io
import os
from datetime import datetime
import json
from jinja2 import Template
from loguru import logger

from httprunner.exceptions import SummaryEmpty
from httprunner import utils


def gen_html_report(summary, now_timestamp, report_template=None, report_dir=None, report_file=None):
    """ render html report with specified report name and template

    Args:
        summary (dict): test result summary data
        report_template (str): specify html report template path, template should be in Jinja2 format.
        report_dir (str): specify html report save directory
        report_file (str): specify html report file path, this has higher priority than specifying report dir.

    """
    if not summary["time"] or summary["stat"]["testcases"]["total"] == 0:
        logger.error(f"test result summary is empty ! {summary}")
        raise SummaryEmpty

    if not report_template:
        report_template = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "thanos_report.html"
        )
        logger.debug("No html report template specified, use default.")
    else:
        logger.info(f"render with html report template: {report_template}")

    logger.info("Start to render Html report ...")

    start_at_timestamp = summary["time"]["start_at"]
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    summary["time"]["start_datetime"] = now_time

    if report_file:
        report_dir = os.path.dirname(report_file)
        report_file_name = os.path.basename(report_file)
    else:
        report_dir = report_dir or os.path.join(os.getcwd(), "reports")
        # fix #826: Windows does not support file name include ":"
        report_file_name = now_timestamp + ".html"


    if not os.path.isdir(report_dir):
        os.makedirs(report_dir)


    report_path = os.path.join(report_dir, report_file_name)
    with io.open(report_template, "r", encoding='utf-8') as fp_r:
        template_content = fp_r.read()
        with io.open(report_path, 'w+', encoding='utf-8') as fp_w:
            rendered_content = Template(
                template_content,
                extensions=["jinja2.ext.loopcontrols"]
            ).render(summary)
            fp_w.write(rendered_content)
    # logger.debug(summary)
    logger.info(f"Generated Html report: {report_path}")

    return report_path


