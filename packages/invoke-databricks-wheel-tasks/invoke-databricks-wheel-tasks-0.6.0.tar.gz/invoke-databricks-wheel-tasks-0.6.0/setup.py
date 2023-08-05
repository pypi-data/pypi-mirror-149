# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invoke_databricks_wheel_tasks', 'invoke_databricks_wheel_tasks.utils']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'databricks-cli>=0.16.4,<0.17.0',
 'invoke>=1.7.0,<2.0.0',
 'poetry-core>=1.0.8,<2.0.0']

setup_kwargs = {
    'name': 'invoke-databricks-wheel-tasks',
    'version': '0.6.0',
    'description': 'Databricks Python Wheel dev tasks in a namespaced collection of tasks to enrich the Invoke CLI task runner.',
    'long_description': '# Invoke Databricks Wheel Tasks\n\nDatabricks Python Wheel dev tasks in a namespaced collection of tasks to enrich the Invoke CLI task runner.\n\n## Getting Started\n\n```sh\npip install invoke-databricks-wheel-tasks\n```\n\nThis will also install `invoke` and `databricks-cli`.\n\n### Databricks CLI Config\n\nIt is assumed you will follow the documentation provided to setup `databricks-cli`.\n\nhttps://docs.databricks.com/dev-tools/cli/index.html\n\nYou\'ll need to setup a Personal Access Token. Then run the following command:\n\n```sh\ndatabricks configure --profile yourprofilename --token\n\nDatabricks Host (should begin with https://): https://myorganisation.cloud.databricks.com/\nToken: \n```\n\nWhich will create a configuration file in your home directory at `~/.databrickscfg` like:\n\n```sh\ncat ~/.databrickscfg\n\n[yourprofilename]\nhost = https://myorganisation.cloud.databricks.com/\ntoken = dapi0123456789abcdef0123456789abcdef\njobs-api-version = 2.1\n```\n\n### Invoke Setup\n\n`tasks.py`\n\n```python\nfrom invoke import task, Collection, Tasks\nimport invoke_databricks_wheel_tasks as db\n\n@task\ndef format(c):\n    """Autoformat code for code style."""\n    c.run("black .")\n    c.run("isort .")\n\n@task\ndef build(c):\n    """Build wheel."""\n    c.run("rm -rfv dist/")\n    c.run("poetry build -f wheel")\n\n# TODO: Find a neater way to capture root tasks as well as setting namespaces\nns = Collection(*[v for v in globals().values() if type(v) == Task])\nns.add_collection(db, name="db")\n```\n\nOnce your `tasks.py` is setup like this `invoke` will have the extra commands:\n\n```sh\nλ invoke --list\nAvailable tasks:\n\n  format         Autoformat code for code style.\n  build          Build wheel.\n  db.runjob          Trigger default job associated for this project.\n  db.reinstall   Reinstall version of wheel on cluster with a restart.\n  db.upload      Upload wheel artifact to DBFS.\n  db.clean       Clean wheel artifact from DBFS.\n```\n\n### Invoke Configuration\n\nEach of the tasks will require some combination of `profile`, `cluster-id`, `job-id` etc.\nYou can create an `invoke.yaml` file which will get loaded into the `invoke` `Context` `Configuration`.\n\nThis will greatly simplify your typing by setting workspace specific flags for your dev iteration loop.\n\n```yaml\n# https://docs.pyinvoke.org/en/latest/concepts/configuration.html\ndatabricks:\n  profile: yourprofilename\n  cluster-id: your-cluster-id-here\n  job-id: 9999\n  artifact-path: "dbfs:/FileStore/wheels/"\n  wheel: "dbfs:/FileStore/wheels/projectname-0.1.0-py3-none-any.whl"\n```\n\n## The Tasks\n\n### db.upload\n\nThis task will use `dbfs` to empty the upload path and then copy the built wheel from `dist/`.\nThis project assumes you\'re using `poetry` or your wheel build output is located in `dist/`.\n\nIf you have other requirements then _pull requests welcome_.\n\n### db.clean\n\nThis tasks will clean up all items on the target `--artifact-path`.\n\n### db.reinstall\n\nAfter some trial and error, creating a job which creates a job cluster everytime is roughly 7 minutes.\n\nHowever if you create an all purpose cluster that you:\n - Mark the old wheel for uninstall\n - restart cluster\n - install updated wheel from dbfs location\n \n This takes roughly 2 minutes which is a much tighter development loop. So these three steps are what `db.reinstall` performs.\n\n### db.runjob\n\nAssuming you have defined a job, that uses a pre-existing cluster, that has your latest wheel installed, this will create a manual trigger of your job with `job-id`.\n\nThe triggering returns a `run-id`, where this `run-id` gets polled until the state gets to an end state.\n\nThen a call to `databricks runs get-output --run-id` happens to retrieve and `error`, `error_trace` and/or `logs` to be emitted to console.\n\n\n## All Together\n\nAssuming, you created your cluster and job definition you may want to create a root level `@task` like:\n\n```python\n@task(pre=[build, db.upload, db.reinstall, db.runjob], default=True)\ndef dev(c):\n  """Default development loop."""\n  ...\n```\n\nYou will notice a few things here:\n\n1. The method has no implementation `...`\n1. We are chaining a series of `@task`s in the `pre=[...]` argument\n1. The `default=True` on this root tasks means we could run either `invoke dev` or simply `invoke`.\n\nHow cool is that?\n\n\n# Contributing\n\nAt all times, you have the power to fork this project, make changes as you see fit and then:\n\n```sh\npip install https://github.com/user/repository/archive/branch.zip\n```\n[Stackoverflow: pip install from github branch](https://stackoverflow.com/a/24811490/622276)\n\nThat way you can run from your own custom fork in the interim or even in-house your work and simply use this project as a starting point. That is totally ok.\n\nHowever if you would like to contribute your changes back, then open a Pull Request "across forks".\n\nOnce your changes are merged and published you can revert to the canonical version of `pip install`ing this package.\n\nIf you\'re not sure how to make changes or if you should sink the time and effort, then open an Issue instead and we can have a chat to triage the issue.\n\n\n# Resources\n\n - [`pyinvoke`](https://pyinvoke.org)\n - [`databricks-cli`](https://docs.databricks.com/dev-tools/cli/index.html)\n\n# Prior Art\n\n - https://github.com/Smile-SA/invoke-sphinx\n - https://github.com/Dashlane/dbt-invoke\n\n',
    'author': 'Josh Peak',
    'author_email': 'neozenith.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/neozenith/invoke-databricks-wheel-tasks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
