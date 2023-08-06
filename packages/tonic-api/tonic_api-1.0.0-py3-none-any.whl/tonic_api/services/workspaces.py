from ..classes.workspace import Workspace
from ..classes.view import View

class WorkspaceService:
    def __init__(self, client):
        self.client = client

    def get_workspace(self, workspace_id):
        workspace = self.client.http_get("/api/workspace/" + workspace_id)
        return Workspace(
            workspace['id'],
            workspace['workspaceName'],
            [View(id, view) for (id, view) in workspace['views'].items()],
            self.client
        )
