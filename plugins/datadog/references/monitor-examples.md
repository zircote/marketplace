# DataDog Monitor Examples

Production-ready monitor configurations for common alerting scenarios.

## High CPU Usage

```python
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_type import MonitorType
from datadog_api_client.v1.model.monitor_options import MonitorOptions
from datadog_api_client.v1.model.monitor_thresholds import MonitorThresholds

def create_high_cpu_monitor():
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)

        monitor = Monitor(
            name="High CPU Usage",
            type=MonitorType("metric alert"),
            query="avg(last_5m):avg:system.cpu.idle{*} by {host} < 20",
            message="""
CPU usage is above 80% on {{host.name}}.

Current idle CPU: {{value}}%
Threshold: <20% idle (>80% usage)

**Runbook**: https://wiki.example.com/runbooks/high-cpu

**Actions**:
1. Check for runaway processes: `top -o cpu`
2. Review recent deployments
3. Scale horizontally if load is legitimate

@slack-alerts @pagerduty
""",
            options=MonitorOptions(
                thresholds=MonitorThresholds(
                    critical=20.0,
                    warning=30.0,
                ),
                notify_no_data=True,
                no_data_timeframe=10,
                require_full_window=True,
                include_tags=True,
                escalation_message="CPU still critical on {{host.name}}. Escalating.",
                renotify_interval=60,
            ),
            tags=["team:platform", "severity:high", "category:infrastructure"],
        )

        response = api.create_monitor(body=monitor)
        print(f"Monitor created: {response.id}")
        return response
```

## Memory Pressure

```python
def create_memory_pressure_monitor():
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)

        monitor = Monitor(
            name="High Memory Usage",
            type=MonitorType("metric alert"),
            query="avg(last_5m):( avg:system.mem.used{*} by {host} / avg:system.mem.total{*} by {host} ) * 100 > 90",
            message="""
Memory usage is above 90% on {{host.name}}.

Current usage: {{value}}%

**Runbook**: https://wiki.example.com/runbooks/high-memory

**Actions**:
1. Check memory consumers: `ps aux --sort=-%mem | head -20`
2. Look for memory leaks in application logs
3. Consider restarting affected services

@slack-alerts
""",
            options=MonitorOptions(
                thresholds=MonitorThresholds(
                    critical=90.0,
                    warning=80.0,
                ),
                notify_no_data=True,
                no_data_timeframe=10,
            ),
            tags=["team:platform", "severity:high", "category:infrastructure"],
        )

        response = api.create_monitor(body=monitor)
        return response
```

## Disk Space

```python
def create_disk_space_monitor():
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)

        monitor = Monitor(
            name="Low Disk Space",
            type=MonitorType("metric alert"),
            query="avg(last_5m):avg:system.disk.in_use{*} by {host,device} * 100 > 85",
            message="""
Disk usage is above 85% on {{host.name}} device {{device.name}}.

Current usage: {{value}}%

**Runbook**: https://wiki.example.com/runbooks/disk-space

**Actions**:
1. Find large files: `du -sh /* | sort -rh | head -20`
2. Clean up logs: `journalctl --vacuum-time=7d`
3. Remove old Docker images: `docker system prune -a`

@slack-alerts
""",
            options=MonitorOptions(
                thresholds=MonitorThresholds(
                    critical=90.0,
                    warning=85.0,
                ),
                notify_no_data=False,
            ),
            tags=["team:platform", "severity:medium", "category:infrastructure"],
        )

        response = api.create_monitor(body=monitor)
        return response
```

## Service Error Rate

```python
def create_error_rate_monitor(service_name: str):
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)

        monitor = Monitor(
            name=f"High Error Rate - {service_name}",
            type=MonitorType("metric alert"),
            query=f"sum(last_5m):sum:trace.http.request.errors{{service:{service_name}}}.as_rate() / sum:trace.http.request.hits{{service:{service_name}}}.as_rate() * 100 > 5",
            message=f"""
Error rate is above 5% for {service_name}.

Current error rate: {{{{value}}}}%

**Runbook**: https://wiki.example.com/runbooks/{service_name}-errors

**Actions**:
1. Check application logs for errors
2. Review recent deployments
3. Check downstream dependencies

@slack-{service_name}-alerts @pagerduty
""",
            options=MonitorOptions(
                thresholds=MonitorThresholds(
                    critical=5.0,
                    warning=2.0,
                ),
                notify_no_data=False,
            ),
            tags=["team:backend", "severity:critical", f"service:{service_name}"],
        )

        response = api.create_monitor(body=monitor)
        return response
```

## Service Latency (P95)

```python
def create_latency_monitor(service_name: str, threshold_ms: float = 500):
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)

        # Convert ms to seconds for DataDog (durations are in seconds)
        threshold_sec = threshold_ms / 1000

        monitor = Monitor(
            name=f"High Latency (P95) - {service_name}",
            type=MonitorType("metric alert"),
            query=f"avg(last_5m):p95:trace.http.request.duration{{service:{service_name}}} > {threshold_sec}",
            message=f"""
P95 latency is above {threshold_ms}ms for {service_name}.

Current P95: {{{{value}}}}s

**Runbook**: https://wiki.example.com/runbooks/{service_name}-latency

**Actions**:
1. Check for slow database queries
2. Review external API call latencies
3. Check for resource contention

@slack-{service_name}-alerts
""",
            options=MonitorOptions(
                thresholds=MonitorThresholds(
                    critical=threshold_sec,
                    warning=threshold_sec * 0.8,
                ),
                notify_no_data=False,
            ),
            tags=["team:backend", "severity:high", f"service:{service_name}"],
        )

        response = api.create_monitor(body=monitor)
        return response
```

## Kubernetes Pod Restarts

```python
def create_pod_restart_monitor():
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)

        monitor = Monitor(
            name="Kubernetes Pod Restarts",
            type=MonitorType("metric alert"),
            query="change(sum:kubernetes.containers.restarts{*} by {pod_name,kube_namespace},last_5m) > 3",
            message="""
Pod {{pod_name.name}} in namespace {{kube_namespace.name}} has restarted more than 3 times in 5 minutes.

Restart count change: {{value}}

**Actions**:
1. Check pod logs: `kubectl logs {{pod_name.name}} -n {{kube_namespace.name}} --previous`
2. Describe pod: `kubectl describe pod {{pod_name.name}} -n {{kube_namespace.name}}`
3. Check for OOMKilled or CrashLoopBackOff

@slack-kubernetes-alerts
""",
            options=MonitorOptions(
                thresholds=MonitorThresholds(
                    critical=3.0,
                    warning=2.0,
                ),
                notify_no_data=False,
            ),
            tags=["team:platform", "severity:high", "category:kubernetes"],
        )

        response = api.create_monitor(body=monitor)
        return response
```

## Database Connection Pool

```python
def create_db_connection_monitor(db_name: str, max_connections: int = 100):
    configuration = Configuration()

    threshold_pct = 80
    threshold = max_connections * threshold_pct / 100

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)

        monitor = Monitor(
            name=f"High Database Connections - {db_name}",
            type=MonitorType("metric alert"),
            query=f"avg(last_5m):avg:postgresql.connections{{db:{db_name}}} > {threshold}",
            message=f"""
Database connection count is above {threshold_pct}% capacity for {db_name}.

Current connections: {{{{value}}}}
Max connections: {max_connections}

**Runbook**: https://wiki.example.com/runbooks/db-connections

**Actions**:
1. Check for connection leaks in application code
2. Review connection pool settings
3. Consider scaling read replicas

@slack-database-alerts
""",
            options=MonitorOptions(
                thresholds=MonitorThresholds(
                    critical=threshold,
                    warning=threshold * 0.9,
                ),
                notify_no_data=True,
                no_data_timeframe=10,
            ),
            tags=["team:data", "severity:high", f"database:{db_name}"],
        )

        response = api.create_monitor(body=monitor)
        return response
```

## Anomaly Detection

```python
def create_anomaly_monitor(service_name: str):
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)

        monitor = Monitor(
            name=f"Anomalous Request Rate - {service_name}",
            type=MonitorType("metric alert"),
            query=f"avg(last_4h):anomalies(sum:trace.http.request.hits{{service:{service_name}}}.as_rate(), 'basic', 3, direction='both') >= 1",
            message=f"""
Anomalous request rate detected for {service_name}.

The request rate is significantly different from historical patterns.

**Actions**:
1. Check for traffic spikes (legitimate or attack)
2. Review deployment changes
3. Verify load balancer health

@slack-{service_name}-alerts
""",
            options=MonitorOptions(
                thresholds=MonitorThresholds(
                    critical=1.0,
                ),
                notify_no_data=False,
                threshold_windows={
                    "trigger_window": "last_15m",
                    "recovery_window": "last_15m",
                },
            ),
            tags=["team:backend", "severity:medium", f"service:{service_name}", "type:anomaly"],
        )

        response = api.create_monitor(body=monitor)
        return response
```

## Composite Monitor (Multi-Condition)

```python
def create_composite_monitor(cpu_monitor_id: int, memory_monitor_id: int):
    """
    Create a composite monitor that triggers when BOTH
    CPU and memory are high simultaneously.
    """
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)

        monitor = Monitor(
            name="Resource Exhaustion (CPU + Memory)",
            type=MonitorType("composite"),
            query=f"{cpu_monitor_id} && {memory_monitor_id}",
            message="""
Both CPU and memory are critically high!

This indicates resource exhaustion requiring immediate action.

**Runbook**: https://wiki.example.com/runbooks/resource-exhaustion

**Immediate Actions**:
1. Scale up horizontally if possible
2. Identify and restart heaviest workloads
3. Consider emergency maintenance window

@pagerduty-critical
""",
            tags=["team:platform", "severity:critical", "category:infrastructure", "type:composite"],
        )

        response = api.create_monitor(body=monitor)
        return response
```

## Monitor Management Utilities

```python
def list_monitors_by_tag(tag: str):
    """List all monitors with a specific tag."""
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)
        response = api.list_monitors(tags=tag)

        for monitor in response:
            print(f"[{monitor.id}] {monitor.name} - {monitor.overall_state}")

        return response


def mute_monitor(monitor_id: int, end_timestamp: int = None):
    """Mute a monitor, optionally until a specific time."""
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)

        if end_timestamp:
            response = api.mute_monitor(monitor_id, end=end_timestamp)
        else:
            response = api.mute_monitor(monitor_id)

        print(f"Monitor {monitor_id} muted")
        return response


def unmute_monitor(monitor_id: int):
    """Unmute a monitor."""
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)
        response = api.unmute_monitor(monitor_id)
        print(f"Monitor {monitor_id} unmuted")
        return response


def delete_monitor(monitor_id: int):
    """Delete a monitor."""
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = MonitorsApi(api_client)
        api.delete_monitor(monitor_id)
        print(f"Monitor {monitor_id} deleted")
```

## Monitor Best Practices

### Thresholds
- Set **warning** thresholds at 80% of critical
- Use `last_5m` for most metrics (avoids noise)
- Use `last_15m` or longer for slowly-changing metrics

### Notifications
- Use `@slack-channel` for team notifications
- Use `@pagerduty` for on-call escalation
- Include **runbook links** in every message
- Add **context variables** like `{{host.name}}`, `{{value}}`

### Tags
- `team:` - Owning team
- `severity:` - critical, high, medium, low
- `service:` - Service name
- `category:` - infrastructure, application, database
- `type:` - metric, anomaly, composite

### Evaluation Windows
| Metric Type | Recommended Window |
|-------------|-------------------|
| CPU/Memory | `last_5m` |
| Error rate | `last_5m` |
| Disk space | `last_15m` |
| Anomaly detection | `last_4h` for training |
| Pod restarts | `last_5m` with `change()` |

### Reduce Alert Fatigue
1. Use composite monitors to correlate signals
2. Set appropriate `renotify_interval` (60+ minutes)
3. Use `require_full_window: True` to avoid edge spikes
4. Implement proper `no_data_timeframe` handling
