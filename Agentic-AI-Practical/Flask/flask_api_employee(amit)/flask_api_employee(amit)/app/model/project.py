class Project:
    """Represents a project in the organization.
    
    This class stores project details including its unique identifier,
    name, and current status. It provides functionality for JSON serialization
    through the to_dict method.
    """
    def __init__(self, project_id, name, status):
        """Initialize a Project object with the provided attributes.
        
        Args:
            project_id (str): Unique project identifier
            name (str): Name of the project
            status (str): Current status of the project (e.g., 'active', 'completed', 'on-hold')
        """
        self.project_id = project_id 
        self.name = name
        self.status = status
        
    def to_dict(self):
        """Convert the Project object to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the project with all attributes
        """
        return {
            "project_id": self.project_id,
            "name": self.name,
            "status": self.status
        }