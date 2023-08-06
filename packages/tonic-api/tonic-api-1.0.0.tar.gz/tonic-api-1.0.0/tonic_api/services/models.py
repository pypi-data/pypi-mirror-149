class ModelService:
    def __init__(self, client):
        self.client = client

    def get_models(self, job_id):
        return self.client.http_get("/api/modeltraining/models/" + job_id)

    def sample(self, model_id, num_rows):
        params = { 'numRows': num_rows } if num_rows is not None else {}
        return self.client.http_get("/api/modeltraining/sample/" + model_id, params=params)

    def sample_source(self, workspace_id, query, num_rows):
        data = { 'workspaceId': workspace_id, 'query':  query, 'numRows': num_rows }
        return self.client.http_post("/api/createview/get_preview_raw", data=data)

    def get_schema(self, workspace_id, query):
        data = { 'workspaceId': workspace_id, 'query':  query }
        return self.client.http_post("/api/createview/get_schema_of_query", data=data)
