from .classes.httpclient import HttpClient
from .services.workspaces import WorkspaceService

class TonicApi:
    def __init__(self, base_url, api_key):
        client = HttpClient(base_url, api_key)
        self.workspace_service = WorkspaceService(client)

    def get_workspace(self, workspace_id):
        return self.workspace_service.get_workspace(workspace_id)
