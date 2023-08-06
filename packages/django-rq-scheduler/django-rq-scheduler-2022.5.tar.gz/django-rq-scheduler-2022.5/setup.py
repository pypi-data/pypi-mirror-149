# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scheduler', 'scheduler.migrations']

package_data = \
{'': ['*']}

install_requires = \
['croniter>=1.2.0,<2.0.0',
 'django-model-utils>=4.2.0,<5.0.0',
 'django-rq>=2.4.1,<3.0.0',
 'django>=4.0',
 'pytz>=2021.3,<2023.0',
 'rq-scheduler>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'django-rq-scheduler',
    'version': '2022.5',
    'description': 'A database backed job scheduler for Django RQ with Django',
    'long_description': "# Django RQ Scheduler \n[![Django CI](https://github.com/dsoftwareinc/django-rq-scheduler/actions/workflows/test.yml/badge.svg)](https://github.com/dsoftwareinc/django-rq-scheduler/actions/workflows/test.yml)\n![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cunla/b756396efb895f0e34558c980f1ca0c7/raw/django-rq-scheduler-4.json)\n\n\nA database backed job scheduler for Django RQ.\nBased on original [django-rq-scheduler](https://github.com/isl-x/django-rq-scheduler) - Now supports Django 4.0.\n\n## Requirements\n\nCurrently, when you pip install Django RQ Scheduler the following packages are also installed.\n\n* django >= 3.2\n* django-model-utils >= 4.2.0\n* django-rq >= 2.4.1\n* rq-scheduler >= 0.11.0\n* pytz >= 2021.3\n* croniter >= 1.2.0\n\nTesting also requires:\n\n* factory_boy >= 2.11.1\n\n\n## Usage\n\n### Install\n\nUse pip to install:\n\n```\npip install django-rq-scheduler\n```\n\n\n### Update Django Settings\n\n1. In `settings.py`, add `django_rq` and `scheduler` to  `INSTALLED_APPS`:\n\n\t```\n\n\tINSTALLED_APPS = [\n    \t...\n    \t'django_rq',\n    \t'scheduler',\n    \t...\n\t]\n\n\n\t```\n\n2. Configure Django RQ. See https://github.com/ui/django-rq#installation\n\n\n### Migrate\n\nThe last step is migrate the database:\n\n```\n./manage.py migrate\n```\n\n## Creating a Job\n\nSee http://python-rq.org/docs/jobs/ or https://github.com/ui/django-rq#job-decorator\n\nAn example:\n\n**myapp.jobs.py**\n\n```\n@job\ndef count():\n    return 1 + 1\n```\n\n## Scheduling a Job\n\n### Scheduled Job\n\n1. Sign into the Django Admin site, http://localhost:8000/admin/ and locate the **Django RQ Scheduler** section.\n\n2. Click on the **Add** link for Scheduled Job.\n\n3. Enter a unique name for the job in the **Name** field.\n\n4. In the **Callable** field, enter a Python dot notation path to the method that defines the job. For the example above, that would be `myapp.jobs.count`\n\n5. Choose your **Queue**. Side Note: The queues listed are defined in the Django Settings.\n\n6. Enter the time the job is to be executed in the **Scheduled time** field. Side Note: Enter the date via the browser's local timezone, the time will automatically convert UTC.\n\n7. Click the **Save** button to schedule the job.\n\n### Repeatable Job\n\n1. Sign into the Django Admin site, http://localhost:8000/admin/ and locate the **Django RQ Scheduler** section.\n\n2. Click on the **Add** link for Repeatable Job\n\n3. Enter a unique name for the job in the **Name** field.\n\n4. In the **Callable** field, enter a Python dot notation path to the method that defines the job. For the example above, that would be `myapp.jobs.count`\n\n5. Choose your **Queue**. Side Note: The queues listed are defined in the Django Settings.\n\n6. Enter the time the first job is to be executed in the **Scheduled time** field. Side Note: Enter the date via the browser's local timezone, the time will automatically convert UTC.\n\n7. Enter an **Interval**, and choose the **Interval unit**. This will calculate the time before the function is called again.\n\n8. In the **Repeat** field, enter the number of time the job is to be ran. Leaving the field empty, means the job will be scheduled to run forever.\n\n9. Click the **Save** button to schedule the job.\n\n\n## Reporting issues or Features\n\nPlease report issues via [GitHub Issues](https://github.com/dsoftwareinc/django-rq-scheduler/issues) .\n\n",
    'author': 'Daniel Moran',
    'author_email': 'daniel.maruani@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dsoftwareinc/django-rq-scheduler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
