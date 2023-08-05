# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt', 'dbt.adapters.athena', 'dbt.include.athena']

package_data = \
{'': ['*'],
 'dbt.include.athena': ['macros/adapters/*',
                        'macros/materializations/models/*',
                        'macros/materializations/models/incremental/*',
                        'macros/materializations/models/table/*',
                        'macros/materializations/models/view/*',
                        'macros/materializations/seeds/*',
                        'macros/materializations/snapshots/*']}

install_requires = \
['boto3==1.20.47',
 'dbt-core>=1.1.0,<1.2.0',
 'pyathena==2.5.2',
 'tenacity==8.0.1']

setup_kwargs = {
    'name': 'dbt-athena2',
    'version': '1.2.2',
    'description': 'Athena adapter for dbt platform',
    'long_description': '# dbt-athena2\nThis is a adapter leveraged from [this repo](https://github.com/Tomme/dbt-athena) to better serve our custom needs. It supports addtional capabilities as below:\n- Run on dbt-core version 1.1.x\n- Support boto3 session to take the credential from from aws profile name\n- On schema change support for new columns added\n- Add s3 bucket for storing data instead of randomly writing on staging dir\n\n## Quick started\nWithin your python environment, proceed below step to initate a first project. There will be some prompts at during inital steps, refer `Configuring your profile` section below to properly set it up.\n\n```bash\npip install dbt-athena2\ndbt init my_dbt_project\nexport DBT_PROFILES_DIR=`pwd`\ncd my_dbt_project\ndbt debug # to test connection\ndbt seed # to dump your seed data\ndbt run # to run all models\ndbt run --select model_name # to run specific model\n\n#...and more...\n```\n\n## Basic usage\n### Model configuration\nBelow show an example how we configure how our model be configured.\n- There are 4 supported `materialized` modes: `view`, `table`, `incremental` and `esphemeral`. Details [here](https://docs.getdbt.com/docs/building-a-dbt-project/building-models/materializations).\n- `incremental_strategy` supports `insert_overwrite` and `append`. If partition is specified, it only overwrites partions available from source data.\n- `on_schema_change` support `fail`, `ignore` and `append_new_columns` only and for only `incremental` materialization. Details [here](https://docs.getdbt.com/docs/building-a-dbt-project/building-models/configuring-incremental-models#understanding-the-is_incremental-macro).\n- There are some usefule macro such as `run_started_at` can be referred from [here](https://docs.getdbt.com/reference/dbt-jinja-functions) to enhance the flexibility on the model.\n\n```yaml\n{{ config(\n    materialized="incremental",\n    partitioned_by=["report_month"],\n    incremental_strategy="insert_overwrite",\n    on_schema_change="append_new_columns"\n) }}\n\n{% set run_date = run_started_at.astimezone(modules.pytz.timezone("Asia/Saigon")).strftime("%Y-%m-%d") %}\n\nselect cast(working_day as timestamp) working_day,\nsum(spend_balance) spend_balance,\nsum(td_balance) td_balance,\nsum(gs_balance) gs_balance,\ncast(date_format(date_parse(\'{{ run_date }}\', \'%Y-%m-%d\') - interval \'1\' month, \'%Y%m\') as int) report_month\nfrom {{ source(\'analytics\', \'eod_balance\') }}\nwhere cast(working_day as date) >= date_trunc(\'month\', cast(date_parse(\'{{ run_date }}\', \'%Y-%m-%d\')  as date)-interval\'2\'month)\nand cast(working_day as date) < date_trunc(\'month\', cast(date_parse(\'{{ run_date }}\', \'%Y-%m-%d\')  as date)-interval\'1\'month)\ngroup by working_day\norder by working_day desc\n```\n\n### Seed\nUnder folder seeds, place csv seed file ( eg. `c_ecom_rate.csv`) and the yaml config (eg. `c_ecom_rate.yml`) as below example. Then run `dbt seed`\n\n```yaml\nversion: 2\n\nseeds:\n  - name: c_ecom_rate\n    config:\n      enabled: true\n      quote_columns: true\n      tags: accounting | report\n```\n\n## Further notes\n- If the workgroup is specified in the `profile.yml` without `s3_staging_dir`, it will extract the default s3 ouput attached with that [`work_group when Override client-side settings enabled`](https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html).\n\n- The boto3 session inherit from devlopment environment; once deployed, it should be obtained permission as role such as EC2 profile instance or K8S service account role.\n\n- Athena limit ALTER ADD COLUMNS with data type `date`, recommend to parse it to `timestamp` or `string` during implementing the model. Details [here](https://docs.aws.amazon.com/athena/latest/ug/alter-table-add-columns.html).\n\n- Athena not accept the comment like `/*`, to ignore these auto generated comment from `dbt`, place this `query-comment: null` in `dbt_project.yml` file.\n\n## Configuring your profile\n\nA dbt profile can be configured to run against AWS Athena using the following configuration:\n\n| Option          | Description                                                                     | Required?  | Example               |\n|---------------- |-------------------------------------------------------------------------------- |----------- |---------------------- |\n| s3_staging_dir  | S3 location to store Athena query results and metadata                          | Required   | `s3://athena-output-bucket/data_services/`    |\n| region_name     | AWS region of your Athena instance                                              | Required   | `ap-southeast-1`           |\n| schema          | Specify the schema (Athena database) to build models into (lowercase **only**)  | Required   | `dbt`                 |\n| database        | Specify the database (Data catalog) to build models into (lowercase **only**)   | Required   | `awsdatacatalog`      |\n| poll_interval   | Interval in seconds to use for polling the status of query results in Athena    | Optional   | `5`                   |\n| aws_profile_name| Profile to use from your AWS shared credentials file.                           | Optional   | `my-profile`          |\n| work_group      | Identifier of Athena workgroup                                                  | Optional   | `my-custom-workgroup` |\n| num_retries     | Number of times to retry a failing query                                        | Optional   | `3`                   |\n| s3_data_dir     | Prefix for storing tables, if different from the connection\'s `s3_staging_dir`  | Optional   | `s3://athena-data-bucket/{schema_name}/{table_name}/`   |\n\n**Example profiles.yml entry:**\n```yaml\nathena:\n  target: dev\n  outputs:\n    dev:\n      database: awsdatacatalog\n      region_name: ap-southeast-1\n      aws_profile_name: dl-dev-process\n      s3_staging_dir: s3://athena-output-bucket/data_services/\n      s3_data_dir: s3://athena-data-bucket/{schema_name}/{table_name}/\n      schema: accounting\n      type: athena\n```\n\n_Additional information_\n* `threads` is supported\n* `database` and `catalog` can be used interchangeably\n\n### Running tests\n\nFirst, install the adapter and its dependencies using `make` (see [Makefile](Makefile)):\n\n```bash\nmake install_deps\n```\n\nNext, configure the environment variables in [dev.env](dev.env) to match your Athena development environment. Finally, run the tests using `make`:\n\n```bash\nmake run_tests\n```\n\n## References\n- [How to structure a dbt project](https://discourse.getdbt.com/t/how-we-structure-our-dbt-projects/355)\n- [dbt best practices](https://docs.getdbt.com/docs/guides/best-practices)',
    'author': 'Duc Nguyen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vdn-tools/dbt-athena2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
