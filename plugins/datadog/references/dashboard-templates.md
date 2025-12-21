# DataDog Dashboard Templates

Ready-to-use dashboard configurations for common monitoring scenarios.

## Service Health Dashboard

```python
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.model.dashboard import Dashboard
from datadog_api_client.v1.model.dashboard_layout_type import DashboardLayoutType
from datadog_api_client.v1.model.widget import Widget
from datadog_api_client.v1.model.widget_definition import WidgetDefinition
from datadog_api_client.v1.model.timeseries_widget_definition import TimeseriesWidgetDefinition
from datadog_api_client.v1.model.timeseries_widget_definition_type import TimeseriesWidgetDefinitionType
from datadog_api_client.v1.model.timeseries_widget_request import TimeseriesWidgetRequest
from datadog_api_client.v1.model.widget_layout import WidgetLayout

SERVICE_NAME = "my-service"  # Replace with your service name

def create_service_health_dashboard():
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = DashboardsApi(api_client)

        dashboard = Dashboard(
            title=f"{SERVICE_NAME} - Service Health",
            description="Request rate, error rate, and latency overview",
            layout_type=DashboardLayoutType.ORDERED,
            widgets=[
                # Request Rate
                Widget(
                    definition=TimeseriesWidgetDefinition(
                        title="Request Rate (req/s)",
                        type=TimeseriesWidgetDefinitionType.TIMESERIES,
                        requests=[
                            TimeseriesWidgetRequest(
                                q=f"sum:trace.http.request.hits{{service:{SERVICE_NAME}}}.as_rate()",
                                display_type="line",
                            )
                        ],
                    ),
                    layout=WidgetLayout(x=0, y=0, width=4, height=3),
                ),
                # Error Rate
                Widget(
                    definition=TimeseriesWidgetDefinition(
                        title="Error Rate (%)",
                        type=TimeseriesWidgetDefinitionType.TIMESERIES,
                        requests=[
                            TimeseriesWidgetRequest(
                                q=f"sum:trace.http.request.errors{{service:{SERVICE_NAME}}}.as_rate() / sum:trace.http.request.hits{{service:{SERVICE_NAME}}}.as_rate() * 100",
                                display_type="line",
                            )
                        ],
                    ),
                    layout=WidgetLayout(x=4, y=0, width=4, height=3),
                ),
                # P95 Latency
                Widget(
                    definition=TimeseriesWidgetDefinition(
                        title="P95 Latency (ms)",
                        type=TimeseriesWidgetDefinitionType.TIMESERIES,
                        requests=[
                            TimeseriesWidgetRequest(
                                q=f"p95:trace.http.request.duration{{service:{SERVICE_NAME}}}",
                                display_type="line",
                            )
                        ],
                    ),
                    layout=WidgetLayout(x=8, y=0, width=4, height=3),
                ),
            ],
        )

        response = api.create_dashboard(body=dashboard)
        print(f"Dashboard created: {response.url}")
        return response
```

## Infrastructure Overview Dashboard

```python
def create_infrastructure_dashboard():
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = DashboardsApi(api_client)

        dashboard = Dashboard(
            title="Infrastructure Overview",
            description="CPU, Memory, Disk, and Network metrics",
            layout_type=DashboardLayoutType.ORDERED,
            widgets=[
                # CPU Usage
                Widget(
                    definition=TimeseriesWidgetDefinition(
                        title="CPU Usage by Host (%)",
                        type=TimeseriesWidgetDefinitionType.TIMESERIES,
                        requests=[
                            TimeseriesWidgetRequest(
                                q="avg:system.cpu.user{*} by {host}",
                                display_type="line",
                            )
                        ],
                    ),
                    layout=WidgetLayout(x=0, y=0, width=6, height=3),
                ),
                # Memory Usage
                Widget(
                    definition=TimeseriesWidgetDefinition(
                        title="Memory Usage by Host (%)",
                        type=TimeseriesWidgetDefinitionType.TIMESERIES,
                        requests=[
                            TimeseriesWidgetRequest(
                                q="avg:system.mem.used{*} / avg:system.mem.total{*} * 100 by {host}",
                                display_type="line",
                            )
                        ],
                    ),
                    layout=WidgetLayout(x=6, y=0, width=6, height=3),
                ),
                # Disk Usage
                Widget(
                    definition=TimeseriesWidgetDefinition(
                        title="Disk Usage by Device (%)",
                        type=TimeseriesWidgetDefinitionType.TIMESERIES,
                        requests=[
                            TimeseriesWidgetRequest(
                                q="avg:system.disk.in_use{*} by {host,device} * 100",
                                display_type="line",
                            )
                        ],
                    ),
                    layout=WidgetLayout(x=0, y=3, width=6, height=3),
                ),
                # Network Traffic
                Widget(
                    definition=TimeseriesWidgetDefinition(
                        title="Network Traffic (bytes/s)",
                        type=TimeseriesWidgetDefinitionType.TIMESERIES,
                        requests=[
                            TimeseriesWidgetRequest(
                                q="avg:system.net.bytes_rcvd{*} by {host}",
                                display_type="line",
                            ),
                            TimeseriesWidgetRequest(
                                q="avg:system.net.bytes_sent{*} by {host}",
                                display_type="line",
                            ),
                        ],
                    ),
                    layout=WidgetLayout(x=6, y=3, width=6, height=3),
                ),
            ],
        )

        response = api.create_dashboard(body=dashboard)
        print(f"Dashboard created: {response.url}")
        return response
```

## Kubernetes Cluster Dashboard

```python
def create_kubernetes_dashboard():
    configuration = Configuration()

    with ApiClient(configuration) as api_client:
        api = DashboardsApi(api_client)

        dashboard = Dashboard(
            title="Kubernetes Cluster Overview",
            description="Pod, container, and node metrics",
            layout_type=DashboardLayoutType.ORDERED,
            widgets=[
                # Running Pods
                Widget(
                    definition=TimeseriesWidgetDefinition(
                        title="Running Pods by Namespace",
                        type=TimeseriesWidgetDefinitionType.TIMESERIES,
                        requests=[
                            TimeseriesWidgetRequest(
                                q="sum:kubernetes.pods.running{*} by {kube_namespace}",
                                display_type="bars",
                            )
                        ],
                    ),
                    layout=WidgetLayout(x=0, y=0, width=6, height=3),
                ),
                # Container Restarts
                Widget(
                    definition=TimeseriesWidgetDefinition(
                        title="Container Restarts",
                        type=TimeseriesWidgetDefinitionType.TIMESERIES,
                        requests=[
                            TimeseriesWidgetRequest(
                                q="sum:kubernetes.containers.restarts{*} by {pod_name}",
                                display_type="line",
                            )
                        ],
                    ),
                    layout=WidgetLayout(x=6, y=0, width=6, height=3),
                ),
                # CPU by Container
                Widget(
                    definition=TimeseriesWidgetDefinition(
                        title="Container CPU Usage",
                        type=TimeseriesWidgetDefinitionType.TIMESERIES,
                        requests=[
                            TimeseriesWidgetRequest(
                                q="avg:kubernetes.cpu.usage.total{*} by {container_name}",
                                display_type="line",
                            )
                        ],
                    ),
                    layout=WidgetLayout(x=0, y=3, width=6, height=3),
                ),
                # Memory by Container
                Widget(
                    definition=TimeseriesWidgetDefinition(
                        title="Container Memory Usage",
                        type=TimeseriesWidgetDefinitionType.TIMESERIES,
                        requests=[
                            TimeseriesWidgetRequest(
                                q="avg:kubernetes.memory.usage{*} by {container_name}",
                                display_type="line",
                            )
                        ],
                    ),
                    layout=WidgetLayout(x=6, y=3, width=6, height=3),
                ),
            ],
        )

        response = api.create_dashboard(body=dashboard)
        print(f"Dashboard created: {response.url}")
        return response
```

## Database Performance Dashboard

```python
def create_database_dashboard(db_type="postgresql"):
    """Create database dashboard. Supports 'postgresql' or 'redis'."""
    configuration = Configuration()

    if db_type == "postgresql":
        widgets = [
            Widget(
                definition=TimeseriesWidgetDefinition(
                    title="Active Connections",
                    type=TimeseriesWidgetDefinitionType.TIMESERIES,
                    requests=[
                        TimeseriesWidgetRequest(
                            q="avg:postgresql.connections{*}",
                            display_type="line",
                        )
                    ],
                ),
                layout=WidgetLayout(x=0, y=0, width=6, height=3),
            ),
            Widget(
                definition=TimeseriesWidgetDefinition(
                    title="Query Duration (avg)",
                    type=TimeseriesWidgetDefinitionType.TIMESERIES,
                    requests=[
                        TimeseriesWidgetRequest(
                            q="avg:postgresql.queries.duration{*}",
                            display_type="line",
                        )
                    ],
                ),
                layout=WidgetLayout(x=6, y=0, width=6, height=3),
            ),
            Widget(
                definition=TimeseriesWidgetDefinition(
                    title="Deadlocks",
                    type=TimeseriesWidgetDefinitionType.TIMESERIES,
                    requests=[
                        TimeseriesWidgetRequest(
                            q="sum:postgresql.deadlocks{*}",
                            display_type="line",
                        )
                    ],
                ),
                layout=WidgetLayout(x=0, y=3, width=6, height=3),
            ),
        ]
        title = "PostgreSQL Performance"
    else:  # redis
        widgets = [
            Widget(
                definition=TimeseriesWidgetDefinition(
                    title="Connected Clients",
                    type=TimeseriesWidgetDefinitionType.TIMESERIES,
                    requests=[
                        TimeseriesWidgetRequest(
                            q="avg:redis.clients.connected{*}",
                            display_type="line",
                        )
                    ],
                ),
                layout=WidgetLayout(x=0, y=0, width=6, height=3),
            ),
            Widget(
                definition=TimeseriesWidgetDefinition(
                    title="Memory Usage",
                    type=TimeseriesWidgetDefinitionType.TIMESERIES,
                    requests=[
                        TimeseriesWidgetRequest(
                            q="avg:redis.mem.used{*}",
                            display_type="line",
                        )
                    ],
                ),
                layout=WidgetLayout(x=6, y=0, width=6, height=3),
            ),
            Widget(
                definition=TimeseriesWidgetDefinition(
                    title="Cache Hit Ratio (%)",
                    type=TimeseriesWidgetDefinitionType.TIMESERIES,
                    requests=[
                        TimeseriesWidgetRequest(
                            q="avg:redis.stats.keyspace_hits{*} / (avg:redis.stats.keyspace_hits{*} + avg:redis.stats.keyspace_misses{*}) * 100",
                            display_type="line",
                        )
                    ],
                ),
                layout=WidgetLayout(x=0, y=3, width=6, height=3),
            ),
        ]
        title = "Redis Performance"

    with ApiClient(configuration) as api_client:
        api = DashboardsApi(api_client)

        dashboard = Dashboard(
            title=title,
            layout_type=DashboardLayoutType.ORDERED,
            widgets=widgets,
        )

        response = api.create_dashboard(body=dashboard)
        print(f"Dashboard created: {response.url}")
        return response
```

## SLO Dashboard

```python
from datadog_api_client.v1.model.slo_widget_definition import SLOWidgetDefinition
from datadog_api_client.v1.model.slo_widget_definition_type import SLOWidgetDefinitionType

def create_slo_dashboard(slo_ids):
    """
    Create SLO dashboard.

    Args:
        slo_ids: List of SLO IDs to display
    """
    configuration = Configuration()

    widgets = []
    for i, slo_id in enumerate(slo_ids):
        widgets.append(
            Widget(
                definition=SLOWidgetDefinition(
                    type=SLOWidgetDefinitionType.SLO,
                    slo_id=slo_id,
                    show_error_budget=True,
                    view_mode="overall",
                    time_windows=["7d", "30d", "90d"],
                ),
                layout=WidgetLayout(x=(i % 2) * 6, y=(i // 2) * 3, width=6, height=3),
            )
        )

    with ApiClient(configuration) as api_client:
        api = DashboardsApi(api_client)

        dashboard = Dashboard(
            title="Service Level Objectives",
            description="SLO compliance and error budget tracking",
            layout_type=DashboardLayoutType.ORDERED,
            widgets=widgets,
        )

        response = api.create_dashboard(body=dashboard)
        print(f"Dashboard created: {response.url}")
        return response
```

## Tips for Dashboard Creation

### Widget Types
- `timeseries` - Time-based line/bar charts
- `query_value` - Single metric value
- `toplist` - Ranked list of values
- `heatmap` - Distribution visualization
- `distribution` - Histogram view
- `slo` - SLO status widget
- `alert_graph` - Monitor alert visualization
- `group` - Container for grouping widgets

### Layout Best Practices
1. Use 12-column grid (width values 1-12)
2. Standard widget heights: 2 (compact), 3 (standard), 4 (detailed)
3. Group related metrics horizontally
4. Put most critical metrics at top-left
5. Use consistent sizing for similar widgets

### Template Variables
```python
from datadog_api_client.v1.model.dashboard_template_variable import DashboardTemplateVariable

dashboard = Dashboard(
    title="My Dashboard",
    template_variables=[
        DashboardTemplateVariable(
            name="service",
            prefix="service",
            default="*",
        ),
        DashboardTemplateVariable(
            name="env",
            prefix="env",
            default="production",
        ),
    ],
    widgets=[...],
)
```

Then use `$service` and `$env` in queries:
```
avg:trace.http.request.duration{service:$service,env:$env}
```
