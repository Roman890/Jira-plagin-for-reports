from jira import JIRA
from datetime import datetime
from configuration import login, api_key, server_url

class Epics:
    project: str
    issue_key: str
    key: str
    summary: str
    assignee: str
    issue_type: str
    status: str
    start_date: str
    due_date: str
    real_date: str
    spend_time: int


class Tasks:
    epic: str
    project: str
    issue_key: str
    key: str
    summary: str
    assignee: str
    issue_type: str
    status: str
    start_date: str
    due_date: str
    real_date: str
    spend_time: int

    def __init__(self):
        pass

class Subtasks:
    task: str
    project: str
    issue_key: str
    key: str
    summary: str
    assignee: str
    issue_type: str
    status: str
    start_date: str
    due_date: str
    real_date: str
    spend_time: int


    def __init__(self):
        pass

def get_epics(project_key, work_date_start_str, work_date_end_str):
    jira_options = {'server': server_url}
    jira = JIRA(options=jira_options, basic_auth=(login,api_key))
    info_list = []
    jql_str = f"project = {project_key} AND type = Эпик AND created >= {work_date_start_str} AND created <= {work_date_end_str} ORDER BY created ASC"
    issues_list = jira.search_issues(jql_str)
    for issue in issues_list:
        epic = Epics()
        epic.project = str(issue.fields.project.name)
        epic.key = issue.key
        epic.issue_key = str(f'=HYPERLINK("{server_url}/browse/{issue.key}","{issue.key}")')
        epic.summary = str(issue.fields.summary)
        epic.issue_type = str(issue.fields.issuetype.name)
        epic.status = str(issue.fields.status.name)
        epic.assignee = str(issue.fields.assignee)
        epic.start_date = str(issue.raw['fields']['customfield_10015'])
        epic.due_date = str(issue.raw['fields']['duedate'])
        epic.real_date = str(issue.raw['fields']['customfield_10029'])
        if issue.raw['fields']['customfield_10029'] is None:
            epic.spend_time = ""
        else:
            epic.spend_time = int(
                date_func(datetime.strptime(str(issue.raw['fields']['customfield_10015']), "%Y-%m-%d"),
                          datetime.strptime(str(issue.raw['fields']['customfield_10029']), "%Y-%m-%d")))
        info_list.append(epic)
    return info_list


def get_tasks(project_key, epics, work_date_start_str, work_date_end_str):
    jira_options = {'server': server_url}
    jira = JIRA(options=jira_options, basic_auth=(login,api_key))
    info_list = []
    for epic in epics:
        jql_str = f"project = {project_key} AND parent={epic.key} AND created >= {work_date_start_str} AND created <= {work_date_end_str} ORDER BY created ASC"
        issues_list = jira.search_issues(jql_str)
        for issue in issues_list:
            task = Tasks()
            task.epic = epic
            task.project = str(issue.fields.project.name)
            task.key = issue.key
            task.issue_key = str(f'=HYPERLINK("{server_url}/browse/{issue.key}","{issue.key}")')
            task.summary = str(issue.fields.summary)
            task.issue_type = str(issue.fields.issuetype.name)
            task.status = str(issue.fields.status.name)
            task.assignee = str(issue.fields.assignee)
            task.start_date = str(issue.raw['fields']['customfield_10015'])
            task.due_date = str(issue.raw['fields']['duedate'])
            task.real_date = str(issue.raw['fields']['customfield_10029'])
            if issue.raw['fields']['customfield_10029'] is None:
                task.spend_time = ""
            else:
                task.spend_time = int(
                    date_func(datetime.strptime(str(issue.raw['fields']['customfield_10015']), "%Y-%m-%d"),
                              datetime.strptime(str(issue.raw['fields']['customfield_10029']), "%Y-%m-%d")))
            info_list.append(task)
    return info_list




def get_subtasks(project_key, tasks, work_date_start_str, work_date_end_str):
    jira_options = {'server': server_url}
    jira = JIRA(options=jira_options, basic_auth=(login,api_key))
    info_list = []
    for task in tasks:
        jql_str = f"project = {project_key} AND parent={task.key} AND created >= {work_date_start_str} AND created <= {work_date_end_str} ORDER BY created ASC"
        issues_list = jira.search_issues(jql_str)
        for issue in issues_list:
            subtask = Subtasks()
            subtask.task = task.key
            subtask.project = str(issue.fields.project.name)
            subtask.key = issue.key
            subtask.issue_key = str(f'=HYPERLINK("{server_url}/browse/{issue.key}","{issue.key}")')
            subtask.summary = str(issue.fields.summary)
            subtask.issue_type = str(issue.fields.issuetype.name)
            subtask.status = str(issue.fields.status.name)
            subtask.assignee = str(issue.fields.assignee)
            subtask.start_date = str(issue.raw['fields']['customfield_10015'])
            subtask.due_date = str(issue.raw['fields']['duedate'])
            subtask.real_date = str(issue.raw['fields']['customfield_10029'])
            if issue.raw['fields']['customfield_10029'] is None:
                subtask.spend_time = ""
            else:
                subtask.spend_time = int(
                    date_func(datetime.strptime(str(issue.raw['fields']['customfield_10015']), "%Y-%m-%d"),
                              datetime.strptime(str(issue.raw['fields']['customfield_10029']), "%Y-%m-%d")))
            info_list.append(subtask)
    return info_list


def get_report_overdue_task(project_key, epics, work_date_start_str, work_date_end_str):
    jira_options = {'server': server_url}
    jira = JIRA(options=jira_options, basic_auth=(login,api_key))
    info_list = []
    for epic in epics:
        jql_str = f"project = {project_key} AND parent={epic.key} AND created >= {work_date_start_str} AND created <= {work_date_end_str} ORDER BY created ASC"
        issues_list = jira.search_issues(jql_str)
        for issue_item in issues_list:
            issue = jira.issue(issue_item.key)
            now = datetime.now()
            if issue.raw['fields']['duedate'] is not None:
                due_date = datetime.strptime(str(issue.raw['fields']['duedate']), "%Y-%m-%d")
                if issue.raw['fields']['customfield_10029'] is None:
                    if (now > due_date):
                        task = Tasks()
                        task.epic = epic
                        task.project = str(issue.fields.project.name)
                        task.key = issue.key
                        task.issue_key = str(f'=HYPERLINK("{server_url}/browse/{issue.key}","{issue.key}")')
                        task.summary = str(issue.fields.summary)
                        task.issue_type = str(issue.fields.issuetype.name)
                        task.status = str(issue.fields.status.name)
                        task.assignee = str(issue.fields.assignee)
                        task.start_date = str(issue.raw['fields']['customfield_10015'])
                        task.due_date = str(issue.raw['fields']['duedate'])
                        task.real_date = str(issue.raw['fields']['customfield_10029'])
                        info_list.append(task)
                else:
                    real_date = datetime.strptime(str(issue.raw['fields']['customfield_10029']), "%Y-%m-%d")
                    if real_date > due_date:
                        task = Tasks()
                        task.epic = epic
                        task.project = str(issue.fields.project.name)
                        task.key = issue.key
                        task.issue_key = str(f'=HYPERLINK("{server_url}/browse/{issue.key}","{issue.key}")')
                        task.summary = str(issue.fields.summary)
                        task.issue_type = str(issue.fields.issuetype.name)
                        task.status = str(issue.fields.status.name)
                        task.assignee = str(issue.fields.assignee)
                        task.start_date = str(issue.raw['fields']['customfield_10015'])
                        task.due_date = str(issue.raw['fields']['duedate'])
                        task.real_date = str(issue.raw['fields']['customfield_10029'])
                        info_list.append(task)
            else:
                continue
    return info_list


def get_report_overdue_subtask(project_key, tasks, work_date_start_str, work_date_end_str):
    jira_options = {'server': server_url}
    jira = JIRA(options=jira_options, basic_auth=(login,api_key))
    info_list = []
    for task in tasks:
        jql_str = f"project = {project_key} AND parent={task.key} AND created >= {work_date_start_str} AND created <= {work_date_end_str} ORDER BY created ASC"
        issues_list = jira.search_issues(jql_str)
        for issue_item in issues_list:
            issue = jira.issue(issue_item.key)
            now = datetime.now()
            if issue.raw['fields']['duedate'] is not None:
                due_date = datetime.strptime(str(issue.raw['fields']['duedate']), "%Y-%m-%d")
                if issue.raw['fields']['customfield_10029'] is None:
                    if (now > due_date):
                        subtask = Subtasks()
                        subtask.task = task.key
                        subtask.project = str(issue.fields.project.name)
                        subtask.key = issue.key
                        subtask.issue_key = str(f'=HYPERLINK("{server_url}/browse/{issue.key}","{issue.key}")')
                        subtask.summary = str(issue.fields.summary)
                        subtask.issue_type = str(issue.fields.issuetype.name)
                        subtask.status = str(issue.fields.status.name)
                        subtask.assignee = str(issue.fields.assignee)
                        subtask.start_date = str(issue.raw['fields']['customfield_10015'])
                        subtask.due_date = str(issue.raw['fields']['duedate'])
                        subtask.real_date = str(issue.raw['fields']['customfield_10029'])
                        info_list.append(subtask)
                else:
                    real_date = datetime.strptime(str(issue.raw['fields']['customfield_10029']), "%Y-%m-%d")
                    if real_date > due_date:
                        subtask = Subtasks()
                        subtask.task = task.key
                        subtask.project = str(issue.fields.project.name)
                        subtask.key = issue.key
                        subtask.issue_key = str(f'=HYPERLINK("{server_url}/browse/{issue.key}","{issue.key}")')
                        subtask.summary = str(issue.fields.summary)
                        subtask.issue_type = str(issue.fields.issuetype.name)
                        subtask.status = str(issue.fields.status.name)
                        subtask.assignee = str(issue.fields.assignee)
                        subtask.start_date = str(issue.raw['fields']['customfield_10015'])
                        subtask.due_date = str(issue.raw['fields']['duedate'])
                        subtask.real_date = str(issue.raw['fields']['customfield_10029'])
                        info_list.append(subtask)
            else:
                continue
    return info_list


def get_report_TTM(project_key, work_date_start_str, work_date_end_str):
    jira_options = {'server': server_url}
    jira = JIRA(options=jira_options, basic_auth=(login,api_key))
    jql_str = f"project = {project_key} AND type = Эпик AND created >= {work_date_start_str} AND created <= {work_date_end_str} ORDER BY created ASC"
    issues_list = jira.search_issues(jql_str)
    info_list = []
    for issue_item in issues_list:
        issue = jira.issue(issue_item.key)
        if ((issue.raw['fields']['customfield_10015'] is not None) and (issue.raw['fields']['duedate'] is not None)):
            days = date_func(datetime.strptime(str(issue.raw['fields']['customfield_10015']), "%Y-%m-%d"), datetime.strptime(str(issue.raw['fields']['duedate']), "%Y-%m-%d"))
            if days > 90:
                data = Tasks()
                data.project_name = str(issue.fields.project.name)
                data.issue_key = str(f'=HYPERLINK("{server_url}/browse/{issue.key}","{issue.key}")')
                data.summary = str(issue.fields.summary)
                data.issue_type = str(issue.fields.issuetype.name)
                data.status = str(issue.fields.status.name)
                data.assignee = str(issue.fields.assignee)
                data.start_date = str(issue.raw['fields']['customfield_10015'])
                data.due_date = str(issue.raw['fields']['duedate'])
                data.real_date = str(issue.raw['fields']['customfield_10029'])
                data.spend_time = ""
                info_list.append(data)
        else:
            continue
    return info_list


def convert_date(date: str):
    return datetime.strptime(date, '%Y-%m-%d')

def date_func(d1, d2):
    return (d2 - d1).days

def create_object(issue):
    data = Tasks()
    data.project_name = str(issue.fields.project.name)
    data.issue_key = str(f'=HYPERLINK("{server_url}/browse/{issue.key}","{issue.key}")')
    data.key = issue.key
    data.summary = str(issue.fields.summary)
    data.issue_type = str(issue.fields.issuetype.name)
    data.status = str(issue.fields.status.name)
    data.assignee = str(issue.fields.assignee)
    data.start_date = str(issue.raw['fields']['customfield_10015'])
    data.due_date = str(issue.raw['fields']['duedate'])
    data.real_date = str(issue.raw['fields']['customfield_10029'])
    data.spend_time = ""
    return data

#get_report_TTM('TeamProject', "2020-07-13", "2020-08-30")