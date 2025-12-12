import json
import os

from utils.decorators import log_exception
from utils.helpers import load_from_json, save_to_json, logger
ROLES_JSON = os.path.join(os.path.dirname(__file__), "..", "json", "roles.json")


class Role:
    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name

    def to_dict(self):
        return vars(self)

    def __str__(self):
        return f"Role [{self.role_id}] - {self.role_name}"

    @log_exception
    @classmethod
    def add_role(cls):
        role_id = input("please enter role id : ")
        role_name = input("please enter role name : ")

        roles = load_from_json(ROLES_JSON)
        role = Role(role_id, role_name).to_dict()
        roles.append(role)
        save_to_json(roles, ROLES_JSON)

    @log_exception
    def list_roles():
        """LIST ALL SAVED ROLES"""
        roles = load_from_json(ROLES_JSON)
        logger.info(f"All Roles loaded...")
        print("\033[92m\nAvailable Roles : ]")
        for r in roles:
            print(f"[{r['role_id']}] {r['role_name']}")
        print("\033[om")