# opentelemetry-resourcedetector-process

An OpenTelemetry package to populates Resource attributes from the running process.

## Usage

```
from opentelemetry.sdk.resources import get_aggregated_resources
from opentelemetry_resourcedetector_process import ProcessResourceDetector

...

resource = get_aggregated_resources([
    ProcessResourceDetector(),
    SomeOtherResourceDetector()
])

... pass the returned `resource` to a TracerProvder, for example ...
```
