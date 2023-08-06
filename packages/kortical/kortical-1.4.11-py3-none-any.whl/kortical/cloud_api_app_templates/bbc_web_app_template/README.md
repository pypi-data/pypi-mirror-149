# bbc_web_app_template
Template for simple Kortical Cloud web application demo.


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

`https://platform.kortical.com/<company_name>/<project_name>/app/bbc_web_app_template/<endpoint>?api_key=o39d20df-1458-4b7d-7291-00461b50c81c`

Where `o39d20df-1458-4b7d-7291-00461b50c81c` is the api_key in this example.

#### predict.yml
The second file that requires some configuration is predict.yml, this contains the configuration for your Kortical predict endpoint.
To find this, you can login to your Kortical system and after selecting deployment from the context menu, select the instance which you wish
to use as your predict endpoint. This will contain both an api_key and a predict_url. Copy these into this configuration file.


### App Deployment
To deploy the app you need to run the following command from inside the bbc_web_app_template directory:

`kortical app deploy --force`

To deploy the app from outside this directory you can run:

`kortical app deploy --app-directory=<app-directory> --force`

where app-directory is the full path to this directory.

The `--force` parameter will overwrite any existing deployment.

### Local Testing

To run the tests found in the `tests` directory you will need to first install this project into your python environment
From inside the `bbc_web_app_template` directory run:

`pip install -e .`

`pip install wheel`

`pip install -r requirements.txt`

This will run the `setup.py` file and install this project as a module. You will now be able to run:

`pytest tests/` or `pytest -m api` from inside the `bbc_web_app_template` directory on your command line to run the tests.

### Local Debugging

If you are using pycharm as your IDE you can use the tests inside `tests/test_api.py` to debug the project.
You will need to set your python interpreter to the virtual environment with this project installed in (run `pip install -e .` inside this project directory to install this project)
By setting your default test runner to pytest, you will then be able to right click on a test and select `Debug "pytest for test_api..."`
