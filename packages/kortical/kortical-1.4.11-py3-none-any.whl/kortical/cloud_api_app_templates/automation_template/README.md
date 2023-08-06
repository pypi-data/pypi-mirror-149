# automation_template
Template for an app to implement an automation workflow.

See the `How To Build an Automation Instant App` tutorial in the Kortical platform documentation for details on configuring the app template.


### Kortical CLI Configuration
You first need to configure your Kortical CLI tool to be pointing to your system, then run this command.

`kortical config init --system-url=<system-url>`

- \<kortical-platform-url\> is similar to: www.platform.kortical.com/<company_name>/<project_name>

(you can find this by looking at your url when you login to the Kortical platform)


### App Deployment
To deploy the app you need to run the following command from inside the bigquery_app_template directory:

`kortical app deploy --force`

To deploy the app from outside this directory you can run:

`kortical app deploy --app-directory=<app-directory> --force`

where app-directory is the full path to this directory.

The `--force` parameter will overwrite any existing deployment.

### Local Testing

To run the tests found in the `tests` directory you will need to first install this project into your python environment
From inside the `automation_template` directory run:

`pip install -e .`

`pip install wheel`

`pip install -r requirements.txt`

This will run the `setup.py` file and install this project as a module. You will now be able to run:

`pytest tests/` or `pytest -m api` from inside the `automation_template` directory on your command line to run the tests.

### Local Debugging

If you are using pycharm as your IDE you can use the tests inside `tests/test_api.py` to debug the project.
You will need to set your python interpreter to the virtual environment with this project installed in (run `pip install -e .` inside this project directory to install this project)
By setting your default test runner to pytest, you will then be able to right click on a test and select `Debug "pytest for test_api..."`
