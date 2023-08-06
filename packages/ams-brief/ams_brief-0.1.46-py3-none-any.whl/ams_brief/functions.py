from datetime import date


def get_project_number(projectpath: str) -> str:
    return str(projectpath)[3:7]


def get_client_and_project(projectpath: str) -> str:
    return str(projectpath)[8:15]


def get_date() -> str:
    return date.today().strftime('%Y%m%d')
