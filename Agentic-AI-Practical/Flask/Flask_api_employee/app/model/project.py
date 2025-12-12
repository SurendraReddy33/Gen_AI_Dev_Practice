class Project:
    def __init__(self, project_id, name, status):
        self.project_id = project_id
        self.name = name
        self.status = status

    def convert_to_dict(self):
        return {
            "project_id": self.project_id,
            "name": self.name,
            "status": self.status
        }