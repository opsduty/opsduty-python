# opsduty-python

> OpsDuty API client.

## Heartbeats

Send periodic heartbeats to OpsDuty using `opsduty-python`. The
heartbeat needs to be configured in OpsDuty before check-ins can
be observed. Head over to [https://opsduty.io](https://opsduty.io)
to configure your heartbeats.

### Alternative 1: Decorator

```python
@heartbeat_checkin(heartbeat="HBXXXX", environment="prod", enabled=True)
def periodic_job():
    pass
```

### Alternative 2: Send heartbeat manually.

```python
def periodic_job():
    try:
        pass
    except Exception:
        print("Job failed.")
    else:
        send_heartbeat_checkin(heartbeat="HBXXXX", environment="prod")
```
