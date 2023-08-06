from more_itertools import first_true
from .training_job import TrainingJob
from ..services.jobs import JobService

class Workspace:
    def __init__(self, id, name, views, client):
        self.id = id
        self.name = name
        self.views = views
        self.client = client
        self.job_service = JobService(client)

    def train(self, force_train):
        if force_train:
            res = self.job_service.start_training(self.id)
            return res['id']
        else:
            try:
                job = self.get_most_recent_training_job('Completed')
                return job.id
            except BaseException as err:
                print("No existing job, starting new one")
                return self.train(True)

    def get_most_recent_training_job(self, status=None):
        job = self.job_service.get_most_recent_job(self.id, 'ModelTraining', status)
        return self.__convert_to_job(job)

    def get_most_recent_training_job_by_view_id(self, view_id):
        return self.__get_most_recent_job_for_view(view_id)

    def get_most_recent_training_job_by_view_name(self, view_name):
        view = first_true(self.views, pred=lambda v: v.name == view_name)
        if view is None:
            raise Exception("No View found by name of " + view_name)
        return self.__get_most_recent_job_for_view(view.id)

    def get_training_job_by_id(self, job_id):
        job = self.job_service.get_job(job_id)
        return self.__convert_to_job(job)

    def get_historical_training_jobs(self):
        jobs = self.job_service.get_jobs(self.id)
        return [self.__convert_to_job(job) for job in jobs]

    def __get_most_recent_job_for_view(self, view_id):
        most_recent_job_per_view = self.job_service.get_most_recent_job_per_view(self.id)
        if view_id not in most_recent_job_per_view:
            raise Exception("No Training Job found for view " + view_id)
        return self.__convert_to_job(most_recent_job_per_view[view_id])

    def __convert_to_job(self, job_json):
        return TrainingJob(job_json['id'], self.id, job_json['publishedTime'], self.client)

    def describe(self):
        print("Workspace: " + self.name + " [" + self.id + "]")
        print("Number of Views: " + str(len(self.views)))
