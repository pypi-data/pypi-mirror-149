# bigquery_app_template
Template for simple Kortical Cloud BigQuery application demo.


### Kortical CLI Configuration
You first need to configure your Kortical CLI tool to be pointing to your system:

`kortical config init --system-url=<system-url>`

- \<kortical-platform-url\> is similar to: www.platform.kortical.com/<company_name>/<project_name>
  
(you can find this by looking at your url when you login to the Kortical platform)

### App Configuration

You will need to set some configuration files before deploying the app, these exist within the `config` directory.

#### authentication.yml
The first one to set will be in the authentication.yml file which contains an api_token, this token is what you will
use to access the endpoint by providing an api_key in the url e.g. 

`https://platform.kortical.com/<company_name>/<project_name>/app/bigquery_app_template/<endpoint>?api_key=o39d20df-1458-4b7d-7291-00461b50c81c`

Where `o39d20df-1458-4b7d-7291-00461b50c81c` is the api_key in this example.

#### predict.yml
The second file that requires some configuration is predict.yml, this contains the configuration for your Kortical predict endpoint.
To find this, you can login to your Kortical system and after selecting deployment from the context menu, select the instance which you wish
to use as your predict endpoint. This will contain both an api_key and a predict_url. Copy these into this configuration file.

#### bigquery/bigquery.py
The third file that will need to be edited based on your specific BigQuery setup is bigquery.py inside src/module_placeholder/bigquery. This file 
currently contains an example which would connect to a table called `speedy_mcgee.titanic.titanic`, where:

    speedy-mcgee - The Google Cloud project
    titanic - Big Query dataset
    titanic - Big Query table

this should be changed to point to your specific BigQuery table.
This file also contains the Schema for the titanic table, this should be updated to match your relevant BigQuery table.

#### bigquery/service_account_key.json
The last piece of configuration you will need to set up is the service_account_key.json file, this is the service account key for 
the GCP service account which has access to your BigQuery instance / table.

The BigQuery permissions this account needs are:
- BigQuery Read Session User at the project level (IAM -> Add -> select service account, select BigQuery Read Session User role)
- BigQuery Data Viewer, when looking at the BigQuery explorer UI-> Select table (view actions-> Open) -> share table -> add BigQuery Data Viewer to the same service account

To be able to write to bigquery tables:
- BigQuery MetaData Viewer - at the project level (required to enumerate the datasets)
- BigQuery Data Editor - at the table level (required to write to the table)

Once your service account has the necessary permissions,
 - go to IAM
 - Service Accounts
 - select Manage Keys for that service account (three dots menu)
 - Add Key
 - Copy this key file into the file service_account_key.json inside the bigquery directory of this project.


### App Deployment
To deploy the app you need to run the following command from inside the bigquery_app_template directory:

`kortical app deploy --force`

To deploy the app from outside this directory you can run:

`kortical app deploy ----app-directory=<app-directory> --force`

where app-directory is the full path to this directory.

The `--force` parameter will overwrite any existing deployment.

### Local Testing

To run the tests found in the `tests` directory you will need to first install this project into your python environment
From inside the `bigquery_app_template` directory run:

`pip install -e .`

`pip install wheel`

`pip install -r requirements.txt`

This will run the `setup.py` file and install this project as a module. You will now be able to run:

`pytest tests/` or `pytest -m api` from inside the `bigquery_app_template` directory on your command line to run the tests.

### Local Debugging

If you are using pycharm as your IDE you can use the tests inside `tests/test_api.py` to debug the project.
You will need to set your python interpreter to the virtual environment with this project installed in (run `pip install -e .` inside this project directory to install this project)
By setting your default test runner to pytest, you will then be able to right click on a test and select `Debug "pytest for test_api..."`
