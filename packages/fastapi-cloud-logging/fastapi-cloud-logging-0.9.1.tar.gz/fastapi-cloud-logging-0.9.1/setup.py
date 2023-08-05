# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_cloud_logging']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.71', 'google-cloud-logging>=3,<4']

setup_kwargs = {
    'name': 'fastapi-cloud-logging',
    'version': '0.9.1',
    'description': 'Cloud Logging For FastAPI',
    'long_description': '# fastapi-cloud-logging\n\n## Project description\n\nfastapi-cloud-logging improves cloud logging with fastapi. It enables to send request data on cloud logging.\n\n## Dependencies\n\n* fastapi\n* cloud logging\n* Python >= 3.7\n  * Require context_vars\n\n## Installation\n\n```sh\npip install fastapi-cloud-logging\n```\n\n## Usage\n\nAdd middleware and handler to send a request info to cloud logging.\n\n```python\nfrom fastapi import FastAPI\nfrom google.cloud.logging import Client\nfrom google.cloud.logging_v2.handlers import setup_logging\n\nfrom fastapi_cloud_logging import FastAPILoggingHandler, RequestLoggingMiddleware\n\napp = FastAPI()\n\n# Add middleware\napp.add_middleware(RequestLoggingMiddleware)\n\n# Use manual handler\nhandler = FastAPILoggingHandler(Client())\nsetup_logging(handler)\n```\n\n```\n{\n  "textPayload": "Hello",\n  "insertId": "198hozmg10qlr8z",\n  "httpRequest": {\n    "requestMethod": "GET",\n    "requestUrl": "http://fastapi-cloud-logging-example-q7ceehebya-an.a.run.app/error",\n    "userAgent": "curl/7.79.1",\n    "remoteIp": "43.235.66.135",\n    "protocol": "http"\n  },\n  "resource": {\n    "type": "cloud_run_revision",\n    "labels": {\n      "location": "asia-northeast1",\n      "project_id": "dauntless-water-347712",\n      "configuration_name": "fastapi-cloud-logging-example",\n      "revision_name": "fastapi-cloud-logging-example-00002-yaf",\n      "service_name": "fastapi-cloud-logging-example"\n    }\n  },\n  "timestamp": "2022-04-26T15:11:47.988375Z",\n  "severity": "ERROR",\n  "labels": {\n    "python_logger": "root"\n  },\n  "logName": "projects/dauntless-water-347712/logs/python",\n  "sourceLocation": {\n    "file": "/app/src/root.py",\n    "line": "22",\n    "function": "error"\n  },\n  "receiveTimestamp": "2022-04-26T15:11:48.006979115Z"\n}\n```\n\n## Appendix\n\n### With Thread\n\nThis is mainly  context\n',
    'author': 'quoth',
    'author_email': '4wordextinguisher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quoth/fastapi-cloud-logging',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
