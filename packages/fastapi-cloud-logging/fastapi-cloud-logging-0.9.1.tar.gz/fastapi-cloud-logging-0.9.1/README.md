# fastapi-cloud-logging

## Project description

fastapi-cloud-logging improves cloud logging with fastapi. It enables to send request data on cloud logging.

## Dependencies

* fastapi
* cloud logging
* Python >= 3.7
  * Require context_vars

## Installation

```sh
pip install fastapi-cloud-logging
```

## Usage

Add middleware and handler to send a request info to cloud logging.

```python
from fastapi import FastAPI
from google.cloud.logging import Client
from google.cloud.logging_v2.handlers import setup_logging

from fastapi_cloud_logging import FastAPILoggingHandler, RequestLoggingMiddleware

app = FastAPI()

# Add middleware
app.add_middleware(RequestLoggingMiddleware)

# Use manual handler
handler = FastAPILoggingHandler(Client())
setup_logging(handler)
```

```
{
  "textPayload": "Hello",
  "insertId": "198hozmg10qlr8z",
  "httpRequest": {
    "requestMethod": "GET",
    "requestUrl": "http://fastapi-cloud-logging-example-q7ceehebya-an.a.run.app/error",
    "userAgent": "curl/7.79.1",
    "remoteIp": "43.235.66.135",
    "protocol": "http"
  },
  "resource": {
    "type": "cloud_run_revision",
    "labels": {
      "location": "asia-northeast1",
      "project_id": "dauntless-water-347712",
      "configuration_name": "fastapi-cloud-logging-example",
      "revision_name": "fastapi-cloud-logging-example-00002-yaf",
      "service_name": "fastapi-cloud-logging-example"
    }
  },
  "timestamp": "2022-04-26T15:11:47.988375Z",
  "severity": "ERROR",
  "labels": {
    "python_logger": "root"
  },
  "logName": "projects/dauntless-water-347712/logs/python",
  "sourceLocation": {
    "file": "/app/src/root.py",
    "line": "22",
    "function": "error"
  },
  "receiveTimestamp": "2022-04-26T15:11:48.006979115Z"
}
```

## Appendix

### With Thread

This is mainly  context
