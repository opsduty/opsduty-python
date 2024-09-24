# opsduty-python

> Command-line utility for interfacing with OpsDuty.

## Heartbeats

Send periodic heartbeats to OpsDuty using `opsduty-python`. The
heartbeat needs to be configured in OpsDuty before check-ins can
be observed. Head over to [https://opsduty.io](https://opsduty.io)
to configure your heartbeats.

### Alternative 1: Decorator

```python
from opsduty_python.heartbeats.heartbeats import (
    heartbeat_checkin,
)

@heartbeat_checkin(heartbeat="HBXXXX", environment="prod", enabled=True)
def periodic_job():
    pass
```

### Alternative 2: Send heartbeat manually.

```python
from opsduty_python.heartbeats.heartbeats import (
    send_heartbeat_checkin,
)

def periodic_job():
    try:
        pass
    except Exception:
        print("Job failed.")
    else:
        send_heartbeat_checkin(heartbeat="HBXXXX", environment="prod")
```
