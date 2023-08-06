class JobService:
    def __init__(self, client):
        self.client = client

    def get_job(self, job_id):
        return self.client.http_get("/api/job/" + job_id)

    def get_jobs(self, workspace_id):
        return self.client.http_get("/api/job/", params={'workspaceId': workspace_id})

    def get_most_recent_job(self, workspace_id, job_type=None, status=None):
        params = {
            'workspaceId': workspace_id,
        }
        if job_type is not None:
            params['type'] = job_type
        if status is not None:
            params['status'] = status
        return self.client.http_get("/api/job/most_recent", params=params)

    def get_most_recent_job_per_view(self, workspace_id):
        return self.client.http_get("/api/modeltraining/most_recent_jobs_per_view", params={'workspaceId': workspace_id})

    def start_training(self, workspace_id):
        return self.client.http_post("/api/modeltraining/train", params={'workspaceId': workspace_id})

    def get_job_status(self, job_id):
        return self.client.http_get("/api/job/" + job_id)
