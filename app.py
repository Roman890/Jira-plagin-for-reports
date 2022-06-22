from flask import Flask, render_template, request, redirect, url_for
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

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    jira_options = {'server': server_url}
    jira = JIRA(options=jira_options, basic_auth=(login, api_key))
    projects = jira.projects()
    return render_template("index.html", projects=projects)


@app.route('/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'POST':
        number = request.form['report']
        project_key = request.form['project']
        date_start_str = request.form['start']
        date_end_str = request.form['end']
        date_start_is_valid = check_date(date_start_str)
        date_end_is_valid = check_date(date_end_str)
        if date_start_is_valid and date_end_is_valid:
            run(int(number), project_key, date_start_str, date_end_str)
    return redirect(url_for('main'))



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


def check_date(date: str):
    if re.search(r'\d{4}-\d{2}-\d{2}', date):
        return True
    return False


if __name__ == "__main__":
    app.run(debug=True)