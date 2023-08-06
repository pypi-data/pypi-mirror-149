import json
import os


def get_initials(employee: str) -> str:
    probe = os.path.join(os.path.dirname(__file__), "data", "employees.json")
    with open(probe) as json_file:
        data = json.load(json_file)
        return data[employee]


initials = get_initials('hanne')
