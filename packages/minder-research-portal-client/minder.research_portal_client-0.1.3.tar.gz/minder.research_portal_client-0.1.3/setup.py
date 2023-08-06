# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minder',
 'minder.research_portal_client',
 'minder.research_portal_client._utils',
 'minder.research_portal_client.api',
 'minder.research_portal_client.models']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['aiohttp[speedups]>=3.8.1,<4.0.0',
 'backoff>=1.11.1,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'minder.research-portal-client',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Research Portal Client\n\nLibrary to interact with Minder Research APIs.\n\n## Example\n\n```bash\npip install minder.research-portal-client\n```\n\n```python\nimport logging\nimport asyncio\nimport datetime\nimport platform\nfrom minder.research_portal_client import Configuration, JobManager\nfrom minder.research_portal_client.models import (\n    ExportJobRequest,\n    ExportJobRequestDataset,\n)\n\n\nlogging.basicConfig(level=logging.INFO)\n\nConfiguration.set_default(\n    Configuration(\n        access_token="---REDACTED---",\n    )\n)\n\n\nasync def example1():\n    async with JobManager() as job_manager:\n        now = datetime.datetime.today()\n        since = now - datetime.timedelta(days=7)\n        datasets: dict(str, ExportJobRequestDataset) = {\n            "patients": ExportJobRequestDataset(),\n            "observation_notes": ExportJobRequestDataset(),\n        }\n\n        export_job = ExportJobRequest(since, datasets=datasets)\n        job_id = await job_manager.submit(export_job)\n        job = await job_manager.wait(job_id)\n        files = await job_manager.download(job)\n        print(files)\n\n\nasync def example2():\n    job_id = "c25249e0-82ff-43d1-9676-f3cead0228b9"\n    async with JobManager() as job_manager:\n        files = await job_manager.download(job_id)\n        print(files)\n\n\nasync def example3():\n    async with JobManager() as job_manager:\n        datasets = await job_manager.client.info.list_datasets()\n        print(datasets)\n\n        organizations = await job_manager.client.info.list_organizations()\n        print(organizations)\n\n        reports = await job_manager.client.reports.list_reports()\n        print(reports)\n\n\nasync def main():\n    await example1()\n    await example2()\n    await example3()\n\n\nif platform.system() == "Windows":\n    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())\n\nasyncio.run(main())\n```\n\n\n\n# Development\n\n## Useful commands\n\n### Setup\n\n```bash\npoetry install\n```\n\n### Run tests\n  \n```bash\npoetry run pytest\n```\n\n### Code Coverage\n\nThis command consists of 2 parts:\n- running tests with coverage collection\n- formatting the report: `report` (text to stdout), `xml` (GitLab compatible: cobertura), `html` (visual)\n\n```bash\npoetry run coverage run -m pytest && poetry run coverage report -m\n```\n\n### Linting\n\n```bash\npoetry run flake8\n```\n\n### Formatting\n\n```bash\npoetry run black .\n```\n\n### Type Checking\n\n```bash\npoetry run mypy .\n```\n',
    'author': 'UK DRI Care Research & Technology centre',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
