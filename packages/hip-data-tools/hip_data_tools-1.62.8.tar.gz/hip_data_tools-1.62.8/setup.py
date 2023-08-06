# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hip_data_tools',
 'hip_data_tools.apache',
 'hip_data_tools.aws',
 'hip_data_tools.etl',
 'hip_data_tools.google',
 'hip_data_tools.hipages',
 'hip_data_tools.oracle']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.28,<0.30.0',
 'GitPython>=3.1.27,<4.0.0',
 'arrow>=1.2.2,<2.0.0',
 'boto3>=1.22.8,<2.0.0',
 'botocore>=1.25.8,<2.0.0',
 'cassandra-driver>=3.25.0,<4.0.0',
 'confluent-kafka>=1.8.2,<2.0.0',
 'fastparquet>=0.8.1,<0.9.0',
 'googleads>=31.0.0,<32.0.0',
 'gspread>=5.3.2,<6.0.0',
 'joblib>=1.1.0,<2.0.0',
 'lxml>=4.7.1,<5.0.0',
 'mysqlclient>=2.1.0,<3.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pyarrow>=8.0.0,<9.0.0',
 'retrying>=1.3.3,<2.0.0',
 'stringcase>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'hip-data-tools',
    'version': '1.62.8',
    'description': 'Common Python tools and utilities for data engineering.',
    'long_description': '# hip-data-tools\n© Hipages Group Pty Ltd 2019-2022\n\n[![PyPI version](https://badge.fury.io/py/hip-data-tools.svg)](https://pypi.org/project/hip-data-tools/#history) \n[![CircleCI](https://circleci.com/gh/hipagesgroup/data-tools/tree/master.svg?style=svg)](https://circleci.com/gh/hipagesgroup/data-tools/tree/master)\n[![Maintainability](https://api.codeclimate.com/v1/badges/bb4c3f9ce84ccec71c76/maintainability)](https://codeclimate.com/repos/5d53b4c199b9430177008586/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/bb4c3f9ce84ccec71c76/test_coverage)](https://codeclimate.com/repos/5d53b4c199b9430177008586/test_coverage)\n\nCommon Python tools and utilities for data engineering, ETL, Exploration, etc. \nThe package is uploaded to PyPi for easy drop and use in various environmnets, such as (but not limited to):\n\n1. Running production workloads\n2. ML Training in Jupyter like notebooks\n3. Local machine for dev and exploration\n\n\n## Installation\nInstall from PyPi repo:\n```bash\npip3 install hip-data-tools\n```\n\nInstall from source\n```bash\npip3 install .\n```\n\n## MacOS Dependencies\n```\nbrew install libev\nbrew install librdkafka\n```\n\n## Connect to aws \n\nYou will need to instantiate an AWS Connection:\n```python\nfrom hip_data_tools.aws.common import AwsConnectionManager, AwsConnectionSettings, AwsSecretsManager\n\n# to connect using an aws cli profile\nconn = AwsConnectionManager(AwsConnectionSettings(region="ap-southeast-2", secrets_manager=None, profile="default"))\n\n# OR if you want to connect using the standard aws environment variables\nconn = AwsConnectionManager(settings=AwsConnectionSettings(region="ap-southeast-2", secrets_manager=AwsSecretsManager(), profile=None))\n\n# OR if you want custom set of env vars to connect\nconn = AwsConnectionManager(\n    settings=AwsConnectionSettings(\n        region="ap-southeast-2",\n        secrets_manager=AwsSecretsManager(\n            access_key_id_var="SOME_CUSTOM_AWS_ACCESS_KEY_ID",\n            secret_access_key_var="SOME_CUSTOM_AWS_SECRET_ACCESS_KEY",\n            use_session_token=True,\n            aws_session_token_var="SOME_CUSTOM_AWS_SESSION_TOKEN"\n            ),\n        profile=None,\n        )\n    )\n\n```\n\nUsing this connection to object you can use the aws utilities, for example aws Athena:\n```python\nfrom hip_data_tools.aws.athena import AthenaUtil\n\nau = AthenaUtil(database="default", conn=conn, output_bucket="example", output_key="tmp/scratch/")\nresult = au.run_query("SELECT * FROM temp limit 10", return_result=True)\nprint(result)\n```\n\n## Connect to Cassandra\n\n ```python\nfrom cassandra.policies import DCAwareRoundRobinPolicy\nfrom cassandra.cqlengine import columns\nfrom cassandra.cqlengine.management import sync_table\nfrom cassandra.cqlengine.models import Model\n\nload_balancing_policy = DCAwareRoundRobinPolicy(local_dc=\'AWS_VPC_AP_SOUTHEAST_2\')\n\nconn = CassandraConnectionManager(\n    settings = CassandraConnectionSettings(\n        cluster_ips=["1.1.1.1", "2.2.2.2"],\n        port=9042,\n        load_balancing_policy=load_balancing_policy,\n    )\n)\n\nconn = CassandraConnectionManager(\n    CassandraConnectionSettings(\n        cluster_ips=["1.1.1.1", "2.2.2.2"],\n        port=9042,\n        load_balancing_policy=load_balancing_policy,\n        secrets_manager=CassandraSecretsManager(\n        username_var="MY_CUSTOM_USERNAME_ENV_VAR"),\n    )\n)\n\n# For running Cassandra model operations\nconn.setup_connection("dev_space")\nclass ExampleModel(Model):\n    example_type    = columns.Integer(primary_key=True)\n    created_at      = columns.DateTime()\n    description     = columns.Text(required=False)\nsync_table(ExampleModel)\n```\n\n## Connect to Google Sheets\n\n#### How to connect\nYou need to go to Google developer console and get credentials. Then the Google sheet need to be shared with client email. GoogleApiConnectionSettings need to be provided with the Google API credentials key json. Then you can access the Google sheet by using the workbook_url and the sheet name.\n\n#### How to instantiate Sheet Util\nYou can instantiate Sheet Util by providing GoogleSheetConnectionManager, workbook_url and the sheet name.\n```python\nsheet_util = SheetUtil(\n    conn_manager=GoogleSheetConnectionManager(self.settings.source_connection_settings),\n    workbook_url=\'https://docs.google.com/spreadsheets/d/cKyrzCBLfsQM/edit?usp=sharing\',\n    sheet=\'Sheet1\')\n```\n\n#### How to read a dataframe using SheetUtil\nYou can get the data in the Google sheet as a Pandas DataFrame using the SheetUtil. We have defined a template for the Google sheet to use with this utility. \n\n![alt text](https://img.techpowerup.org/200311/screen-shot-2020-03-11-at-4-08-25-pm.png)\n\nYou need to provide the "field_names_row_number" and "field_types_row_number" to call "get_dataframe()" method in SheetUtil.\n\n```python\nsheet_data = sheet_util.get_data_frame(\n                field_names_row_number=8,\n                field_types_row_number=7,\n                row_range="12:20",\n                data_start_row_number=9)\n```\n\n\n\nYou can use load_sheet_to_athena() function to load Google sheet data into an Athena table.\n\n```python\nGoogleSheetToAthena(GoogleSheetsToAthenaSettings(\n        source_workbook_url=\'https://docs.google.com/spreadsheets/d/cKyrzCBLfsQM/edit?usp=sharing\',\n        source_sheet=\'spec_example\',\n        source_row_range=None,\n        source_fields=None,\n        source_field_names_row_number=5,\n        source_field_types_row_number=4,\n        source_data_start_row_number=6,\n        source_connection_settings=get_google_connection_settings(gcp_conn_id=GCP_CONN_ID),\n        manual_partition_key_value={"column": "start_date", "value": START_DATE},\n        target_database=athena_util.database,\n        target_table_name=TABLE_NAME,\n        target_s3_bucket=s3_util.bucket,\n        target_s3_dir=s3_dir,\n        target_connection_settings=get_aws_connection_settings(aws_conn_id=AWS_CONN_ID),\n        target_table_ddl_progress=False\n    )).load_sheet_to_athena()\n```\n\nThere is an integration test called "integration_test_should__load_sheet_to_athena__when_using_sheetUtil" to test this functionality. You can simply run it by removing the "integration_" prefix.\n',
    'author': 'Hipages Data Team',
    'author_email': 'datascience@hipagesgroup.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
