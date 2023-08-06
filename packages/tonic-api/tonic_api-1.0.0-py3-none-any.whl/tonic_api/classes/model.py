from ..services.models import ModelService
import pandas as pd

class Model:
    def __init__(self, id, job_id, workspace_id, view, client):
        self.id = id
        self.job_id = job_id
        self.workspace_id = workspace_id
        self.view = view
        self.model_service = ModelService(client)

    def sample(self, num_rows=None):
        res = self.model_service.sample(self.id, num_rows)
        return self.__convert_to_df(res)

    def sample_source(self, num_rows=None):
        n_rows_to_sample = num_rows if num_rows is not None else 1
        res = self.model_service.sample_source(self.workspace_id, self.view.query, n_rows_to_sample)
        columns = res['columns']
        if len(columns) == 0:
            raise Exception("No data returned from source database")

        n_rows_returned = len(columns[0]['data'])
        converted_res = [{} for _ in range(n_rows_returned)]

        if n_rows_returned < n_rows_to_sample:
            print("Not enough rows in source destination to sample, limiting to " + str(n_rows_returned) + " rows.")

        for col in columns:
            data = col['data']
            for idx, val in enumerate(data):
                converted_res[idx][col['columnName']] = val
        return self.__convert_to_df(converted_res)

    def get_numeric_columns(self):
        return [col for (col, encoding) in self.view.encodings.items() if encoding == 'Numeric']

    def get_categorical_columns(self):
        return [col for (col, encoding) in self.view.encodings.items() if encoding == 'Categorical']

    def __convert_to_df(self, sample_response):
        schema = self.__get_schema()
        df = pd.DataFrame(sample_response)
        df = self.__conform_df_to_schema(df, schema)
        return df

    def __get_schema(self):
        schema = self.model_service.get_schema(self.workspace_id, self.view.query)
        ordered_schema = self.__convert_schema_to_ordered_col_list(schema)
        return ordered_schema

    def __convert_schema_to_ordered_col_list(self, schema):
        return [obj["columnName"] for obj in sorted(schema, key=lambda v: v["ordinalPosition"])]

    def __conform_df_to_schema(self, df, schema):
        return df.reindex(schema, axis=1)

    def describe(self):
        print("Model: [" + self.id + "]")
        print("Job ID: " + self.job_id)
        print("Workspace ID: " + self.workspace_id)
        print("Model View: ")
        self.view.describe()
