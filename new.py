from jira import JIRA
from configuration import server_url, api_key, login
import os
import sys
import re
import subprocess
import reporter
import xls_spendtime
import xls_overdue
import xls_TTM

def run(number, project_key, date_start_str, date_end_str):
    excel_filename = ""
    if number is 1:
        epics_list = reporter.get_epics(project_key, date_start_str, date_end_str)
        tasks_list = reporter.get_tasks(project_key, epics_list, date_start_str, date_end_str)
        subtasks_list = reporter.get_subtasks(project_key, tasks_list, date_start_str, date_end_str)
        excel_filename = xls_spendtime.write_report(epics_list, tasks_list, subtasks_list, f"{date_start_str}-{date_end_str}")
    if number is 2:
        epics_list = reporter.get_epics(project_key, date_start_str, date_end_str)
        tasks_list = reporter.get_report_overdue_task(project_key, epics_list, date_start_str, date_end_str)
        subtasks_list = reporter.get_report_overdue_subtask(project_key, tasks_list, date_start_str, date_end_str)
        excel_filename = xls_overdue.write_report(epics_list, tasks_list, subtasks_list, f"{date_start_str}-{date_end_str}")
    if number is 3:
        issue_list = reporter.get_report_TTM(project_key, date_start_str, date_end_str)
        excel_filename = xls_TTM.write_report(issue_list, f"{date_start_str}-{date_end_str}")

    if sys.platform.startswith('darwin'):
        subprocess.call(('open', excel_filename))
    elif os.name == 'nt':
        os.startfile(excel_filename)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', excel_filename))

run(2,"TeamProject", "2020-07-06", "2020-07-28" )