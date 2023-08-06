from more_itertools import first_true
from datetime import datetime
import time
import re
from ..services.jobs import JobService
from ..services.models import ModelService
from .model import Model
from .view import View

class TrainingJob:
    def __init__(self, id, workspace_id, published_time, client):
        self.id = id
        self.workspace_id = workspace_id
        self.published_time = published_time
        self.client = client
        self.job_service = JobService(client)
        self.model_service = ModelService(client)

    def get_training_status(self):
        job = self.job_service.get_job_status(self.id)
        return TrainingStatus(job)

    def tail_training_status(self):
        status = None
        status_messages = []
        last_epoch_metadata_by_view = {}
        while status is None or status.state != "Completed":
            status = self.get_training_status()

            if status.state == "Completed":
                # Show the final epoch training status on completion
                status_messages, last_epoch_metadata_by_view = self.__handle_epoch_updates(status, last_epoch_metadata_by_view, True)
                status_messages.append("Training completed")
                break;
            elif status.state == "Failed":
                status_messages = ["Training failed: " + status.error]
                break
            elif status.state == "Canceled":
                status_messages = ["Training was canceled by user"]
                break
            elif status.state == "Running":
                status_messages, last_epoch_metadata_by_view = self.__handle_epoch_updates(status, last_epoch_metadata_by_view)
            else:
                status_messages = ["Training status: " + status.state]

            self.__print_with_timestamp(status_messages)

            time.sleep(5)

        # Last message(s)
        self.__print_with_timestamp(status_messages)

    def get_trained_models(self):
        models = self.model_service.get_models(self.id)
        return [self.__convert_to_model(model) for model in models]

    def get_trained_model_by_view_id(self, view_id):
        models_json = self.model_service.get_models(self.id)
        models = [self.__convert_to_model(model) for model in models_json]
        model = first_true(models, pred=lambda m: m.view.id == view_id)
        if model is None:
            raise Exception("No model for view ID " + view_id + " found")
        return model

    def get_trained_model_by_view_name(self, view_name):
        models_json = self.model_service.get_models(self.id)
        models = [self.__convert_to_model(model) for model in models_json]
        model = first_true(models, pred=lambda m: m.view.name == view_name)
        if model is None:
            raise Exception("No model for view name " + view_name + " found")
        return model

    def describe(self):
        print("Training Job: " + self.id + " [Published at " + self.published_time + "]")
        print("Workspace ID: " + self.workspace_id)

    def __convert_to_model(self, model_json):
        return Model(model_json['modelId'], self.id, self.workspace_id, View(model_json['viewId'], model_json['view']), self.client)

    def __print_with_timestamp(self, messages):
        now = datetime.now().strftime("%D %H:%M:%S")
        for message in messages:
            print("[" + now + "] " + message)

    def __handle_epoch_updates(self, status, last_epoch_metadata_by_view, update_existing_only=False):
        status_messages = []

        epoch_metadata_by_view = status.current_epoch_progress()
        if epoch_metadata_by_view is not None:
            for view, epoch_metadata in epoch_metadata_by_view.items():
                # Only print when epoch has updated
                if not update_existing_only and (view not in last_epoch_metadata_by_view or epoch_metadata[0] != last_epoch_metadata_by_view[view][0]):
                    status_messages.append("Training status: Running " + view + " (" + epoch_metadata[0] + "/" + epoch_metadata[1] + " epochs completed)")
                    last_epoch_metadata_by_view[view] = epoch_metadata
                elif update_existing_only and view in last_epoch_metadata_by_view and epoch_metadata[0] != last_epoch_metadata_by_view[view][0]:
                    status_messages.append("Training status: Running " + view + " (" + epoch_metadata[0] + "/" + epoch_metadata[1] + " epochs completed)")
                    last_epoch_metadata_by_view[view] = epoch_metadata
        else:
            status_messages = ["Training status: Running (no training tasks reported yet)"]

        return status_messages, last_epoch_metadata_by_view

class TrainingStatus:
    def __init__(self, job_json):
        self.state = job_json['status']
        self.error = job_json['errorMessages'] if 'errorMessages' in job_json else None
        self.tasks = job_json['tasks'] if 'tasks' in job_json else None

    def current_epoch_progress(self):
        epoch_metadata_by_view = {}
        if self.tasks is not None:
            epoch_tasks = [task for task in self.tasks if 'Training AI Synthesizer Model' in task['action']]
            for task in epoch_tasks:
                regex = re.match("^Training AI Synthesizer Model for (\w+)$", task['action'])
                if regex is not None:
                    view_name = regex.group(1)
                    if 'stepsCompleted' in task and 'totalSteps' in task:
                        epoch_metadata_by_view[view_name] = (str(task['stepsCompleted']), str(task['totalSteps']))
            return epoch_metadata_by_view
        return None

    def describe(self):
        print("Job status: " + self.state)
        if self.error is not None:
            print('Job failed due to: "' + self.error + '"')
