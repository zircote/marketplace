# datadog Plugin

DataDog API specialists for monitoring setup, dashboard creation, metric queries, and APM integration with production-ready code patterns.

## Installation

```bash
claude /plugin marketplace add zircote/marketplace
claude /plugin install datadog
```

## Quick Start

Get started with common DataDog tasks:

### Create a Monitor
```
Using the datadog-api-expert agent, create a monitor for:
- High CPU usage (>80% for 5 minutes)
- Alert via Slack to #alerts channel
- Include runbook link in notification
```

### Query Metrics
```
Using the datadog-pro agent, show me:
- Average response time for my-service over last hour
- Error rate trend for the past 24 hours
- P95 latency broken down by endpoint
```

### Build a Dashboard
```
Using the datadog-pro agent, create a dashboard with:
- Service health overview (request rate, error rate, latency)
- Infrastructure metrics (CPU, memory, disk)
- Top 10 slowest endpoints table
```

### Search Logs
```
Using the datadog-api-expert agent:
- Search for errors in production over the last hour
- Aggregate logs by service and status
- Find all 5xx responses for my-api
```

## Common Query Patterns

| Use Case | Query |
|----------|-------|
| High CPU | `avg:system.cpu.user{*} > 80` |
| Memory pressure | `avg:system.mem.used{*} / avg:system.mem.total{*} > 0.9` |
| Error rate | `sum:trace.http.request.errors{service:my-service}.as_rate()` |
| Request latency P95 | `p95:trace.http.request.duration{service:my-service}` |
| Disk usage | `avg:system.disk.in_use{*} > 0.85` |
| Container restarts | `sum:kubernetes.containers.restarts{*}` |

## Verify Installation

After installing, test the agents are working:

```bash
claude "Using the datadog-pro agent, explain how to authenticate with the DataDog API"
```

You should see a complete response with code examples and documentation links.

## Contents

### Agents

#### datadog-pro
Expert DataDog API specialist for Python `datadog-api-client` library (v2.45.0+).

**Use PROACTIVELY for:**
- Monitoring setup and configuration
- DataDog integration patterns
- Dashboard creation and management
- API troubleshooting and debugging

#### datadog-api-expert
Specialized DataDog API expert with focus on:
- Monitor and dashboard creation
- API troubleshooting and query syntax
- v1/v2 API handling
- Authentication and error handling patterns

## Features

Both agents provide:

- **Complete Code Examples**: Runnable code with all imports and error handling
- **API Version Guidance**: Clear distinction between v1 (stable) and v2 (unstable) APIs
- **Official Documentation Citations**: References to DataDog docs for every pattern
- **Production-Ready Patterns**: Context managers, error handling, pagination

## API Coverage

### v1 API (Stable)
- MonitorsApi - Create and manage alerts
- DashboardsApi - Build monitoring dashboards
- MetricsApi - Query and submit metrics
- HostsApi - Manage host metadata
- DowntimesApi - Schedule maintenance windows
- EventsApi - Create and query events
- SLOsApi - Define service level objectives

### v2 API (Modern/Unstable)
- IncidentsApi - Incident management
- SecurityMonitoringApi - Security signals
- CaseManagementApi - Case tracking
- LogsApi - Log queries and aggregation
- RUMApi - Real User Monitoring

## Usage Examples

### Create a Monitor

```python
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_type import MonitorType

configuration = Configuration()

with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    monitor = Monitor(
        name="High CPU Usage",
        type=MonitorType("metric alert"),
        query="avg(last_5m):avg:system.cpu.idle{*} < 20",
        message="CPU usage is above 80%! @pagerduty",
    )
    response = api_instance.create_monitor(body=monitor)
```

### Query Metrics

```python
from datadog_api_client.v1.api.metrics_api import MetricsApi
import time

start = int(time.time()) - 3600
end = int(time.time())
response = api_instance.query_metrics(
    _from=start,
    to=end,
    query="avg:system.cpu.idle{*}",
)
```

### Create a Dashboard

```python
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.model.dashboard import Dashboard
from datadog_api_client.v1.model.dashboard_layout_type import DashboardLayoutType

dashboard = Dashboard(
    title="Application Metrics",
    layout_type=DashboardLayoutType.ORDERED,
    widgets=[
        # Widget definitions...
    ],
)
response = api_instance.create_dashboard(body=dashboard)
```

## Authentication

Set environment variables:

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-app-key"
```

Both keys are required for most operations.

## Regional Configuration

```python
configuration = Configuration()
configuration.server_variables["site"] = "datadoghq.eu"  # For EU region

# Available regions:
# - datadoghq.com (US1, default)
# - us3.datadoghq.com (US3)
# - us5.datadoghq.com (US5)
# - datadoghq.eu (EU1)
# - ap1.datadoghq.com (AP1)
# - ddog-gov.com (US Government)
```

## Integration with Other Plugins

These agents integrate with:

| Plugin | Integration |
|--------|-------------|
| **z plugin** | `sre-engineer` for reliability engineering |
| **z plugin** | `devops-engineer` for infrastructure setup |
| **z plugin** | `performance-engineer` for observability workflows |

## Version

**Plugin:** 1.0.0
