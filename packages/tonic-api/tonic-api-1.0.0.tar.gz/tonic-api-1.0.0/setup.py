# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tonic_api', 'tonic_api.classes', 'tonic_api.services']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.6.0,<9.0.0',
 'pandas>=1.0.0,<2.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'tonic-api',
    'version': '1.0.0',
    'description': 'Wrappers around the Tonic.ai API',
    'long_description': '# Overview\nThis library contains useful wrappers around the Tonic.ai API.\n\n## Usage\n\nInstantiate the API wrapper using the following code:\n\n```\nfrom tonic_api.api import TonicApi\n\n# Do not include trailing backslash in TONIC_URL\napi = TonicApi(TONIC_URL, API_KEY)\n```\n\nOnce instantiated, the following endpoints are available for consumption. Note that available endpoints and response types are limited. Available fields may be severely limited compared to the current Tonic API.\n\n```\nTonicApi:\n    get_workspace(workspace_id) => Workspace\n\nWorkspace:\n    id => string\n    name => string\n    views => View[]\n\n    train(force_train) => existing or new job ID (if force_train or no Completed jobs)\n    get_most_recent_training_job(with_status) => TrainingJob (by default any status)\n    get_most_recent_training_job_by_view_id(view_id) => TrainingJob\n    get_most_recent_training_job_by_view_name(view_name) => TrainingJob\n    get_training_job_by_id(job_id) => TrainingJob\n    get_historical_training_jobs() => TrainingJob[]\n\n    describe() => debugger helper for printing fields\n\nView:\n    id => string\n    name => string\n    query => string\n    parameters => {}\n    encodings => {}\n\n    describe() => debugger helper for printing fields\n\nTrainingJob:\n    id => string\n    published_time => string\n\n    get_training_status() => TrainingStatus\n    tail_training_status() => tails and prints status updates on training\n    get_trained_models() => Model[]\n    get_trained_model_by_view_id(view_id) => Model\n    get_trained_model_by_view_name(view_name) => Model\n\n    describe() => debugger helper for printing fields\n\nModel:\n    id => string\n    view => View\n\n    sample(num_rows) => pandas DataFrame (defaults to 1 row if num_rows not provided)\n    sample_source(num_rows) => pandas DataFrame (defaults to 1 row if num_rows not provided). Note: NOT randomized. Upper limit is limited to row count in source.\n\n    get_numeric_columns() => string[]\n    get_categorical_columns() => string[]\n\n    describe() => debugger helper for printing fields\n```\n',
    'author': 'Eric Timmerman',
    'author_email': 'eric@tonic.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.tonic.ai/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
