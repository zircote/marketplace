# Common DataDog Queries

Quick reference for frequently used DataDog metric queries.

## System Metrics

### CPU
```
# Average CPU usage across all hosts
avg:system.cpu.user{*}

# CPU by host
avg:system.cpu.user{*} by {host}

# High CPU alert threshold
avg(last_5m):avg:system.cpu.idle{*} < 20

# CPU iowait (disk bottleneck indicator)
avg:system.cpu.iowait{*}
```

### Memory
```
# Memory usage percentage
avg:system.mem.used{*} / avg:system.mem.total{*} * 100

# Available memory
avg:system.mem.usable{*}

# Memory pressure alert
avg(last_5m):( avg:system.mem.used{*} / avg:system.mem.total{*} ) > 0.9

# Swap usage
avg:system.swap.used{*}
```

### Disk
```
# Disk usage percentage
avg:system.disk.in_use{*}

# Disk usage by device
avg:system.disk.in_use{*} by {device}

# Disk I/O
avg:system.io.r_s{*}, avg:system.io.w_s{*}

# Disk space alert
avg(last_5m):avg:system.disk.in_use{*} by {host,device} > 0.85
```

### Network
```
# Network bytes in/out
avg:system.net.bytes_rcvd{*}, avg:system.net.bytes_sent{*}

# Network errors
sum:system.net.errors.in{*}, sum:system.net.errors.out{*}

# Network packets
rate(sum:system.net.packets_in.count{*}), rate(sum:system.net.packets_out.count{*})
```

## Application Performance (APM)

### Request Metrics
```
# Request rate
sum:trace.http.request.hits{service:my-service}.as_rate()

# Error rate
sum:trace.http.request.errors{service:my-service}.as_rate()

# Error percentage
sum:trace.http.request.errors{service:my-service}.as_rate() /
sum:trace.http.request.hits{service:my-service}.as_rate() * 100

# Latency percentiles
p50:trace.http.request.duration{service:my-service}
p95:trace.http.request.duration{service:my-service}
p99:trace.http.request.duration{service:my-service}
```

### By Endpoint
```
# Requests by resource (endpoint)
sum:trace.http.request.hits{service:my-service} by {resource}

# Latency by endpoint
avg:trace.http.request.duration{service:my-service} by {resource}

# Top 10 slowest endpoints
top(avg:trace.http.request.duration{service:my-service} by {resource}, 10, 'mean', 'desc')
```

### By Status Code
```
# Requests by HTTP status
sum:trace.http.request.hits{service:my-service} by {http.status_code}

# 5xx errors only
sum:trace.http.request.hits{service:my-service,http.status_code:5*}

# 4xx errors only
sum:trace.http.request.hits{service:my-service,http.status_code:4*}
```

## Kubernetes Metrics

### Pods
```
# Running pods by namespace
sum:kubernetes.pods.running{*} by {kube_namespace}

# Pod restarts
sum:kubernetes.containers.restarts{*} by {pod_name}

# Pod restart alert
change(sum:kubernetes.containers.restarts{*} by {pod_name}, last_5m) > 3
```

### Containers
```
# Container CPU usage
avg:kubernetes.cpu.usage.total{*} by {container_name}

# Container memory usage
avg:kubernetes.memory.usage{*} by {container_name}

# Container memory limit percentage
avg:kubernetes.memory.usage{*} by {container_name} /
avg:kubernetes.memory.limits{*} by {container_name} * 100
```

### Nodes
```
# Node CPU allocatable
avg:kubernetes.cpu.capacity{*} by {host}

# Node memory pressure
avg:kubernetes.memory.usage{*} by {host} / avg:kubernetes.memory.capacity{*} by {host}
```

## Database Metrics

### PostgreSQL
```
# Active connections
avg:postgresql.connections{*}

# Connection utilization
avg:postgresql.connections{*} / avg:postgresql.max_connections{*} * 100

# Query duration
avg:postgresql.queries.duration{*}

# Deadlocks
sum:postgresql.deadlocks{*}
```

### Redis
```
# Connected clients
avg:redis.clients.connected{*}

# Memory usage
avg:redis.mem.used{*}

# Cache hit ratio
avg:redis.stats.keyspace_hits{*} /
(avg:redis.stats.keyspace_hits{*} + avg:redis.stats.keyspace_misses{*}) * 100

# Keys evicted
sum:redis.keys.evicted{*}
```

## Custom Metrics

### Counters (use .as_rate())
```
# Events per second
sum:my.custom.event.count{*}.as_rate()

# Events by type
sum:my.custom.event.count{*}.as_rate() by {event_type}
```

### Gauges
```
# Current queue depth
avg:my.queue.depth{*}

# Queue depth by queue name
avg:my.queue.depth{*} by {queue_name}
```

### Histograms
```
# Percentiles
p50:my.custom.duration{*}
p95:my.custom.duration{*}
p99:my.custom.duration{*}

# Average with outlier filtering
avg:my.custom.duration{*}.rollup(avg, 60)
```

## Query Modifiers

### Time Aggregation
```
.rollup(avg, 300)   # 5-minute average
.rollup(sum, 3600)  # Hourly sum
.rollup(max, 86400) # Daily maximum
```

### Space Aggregation
```
avg:metric{*}           # Average across all
sum:metric{*}           # Sum across all
max:metric{*}           # Maximum across all
min:metric{*}           # Minimum across all
```

### Functions
```
rate(metric)            # Rate of change
diff(metric)            # Difference from previous
abs(metric)             # Absolute value
log2(metric)            # Logarithm base 2
derivative(metric)      # Derivative
integral(metric)        # Integral over time
```

### Comparisons
```
top(metric, 10, 'mean', 'desc')    # Top 10 by mean
bottom(metric, 5, 'mean', 'asc')   # Bottom 5 by mean
forecast(metric, 'linear', 1)      # Linear forecast
anomalies(metric, 'basic', 2)      # Anomaly detection
```
