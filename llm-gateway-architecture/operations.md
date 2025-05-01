# LLM Gateway Operations Guide

This document provides information on deploying, configuring, monitoring, and troubleshooting the LLM Gateway.

## Table of Contents

- [Deployment](#deployment)
  - [Prerequisites](#prerequisites)
  - [Kubernetes Deployment](#kubernetes-deployment)
  - [Docker Deployment](#docker-deployment)
  - [Standalone Deployment](#standalone-deployment)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Service Properties](#service-properties)
  - [Logging Configuration](#logging-configuration)
  - [Metrics Configuration](#metrics-configuration)
- [Scaling](#scaling)
  - [Horizontal Scaling](#horizontal-scaling)
  - [Vertical Scaling](#vertical-scaling)
  - [Resource Recommendations](#resource-recommendations)
- [Monitoring](#monitoring)
  - [Health Checks](#health-checks)
  - [Metrics](#metrics)
  - [Logs](#logs)
  - [Alerts](#alerts)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
  - [Debugging Tools](#debugging-tools)
  - [Support](#support)

## Deployment

### Prerequisites

Before deploying the LLM Gateway, ensure the following prerequisites are met:

- Java 11 or higher
- MariaDB/MySQL 5.7 or higher
- Redis 6.x or higher (for caching)
- Prometheus (for metrics collection)
- Kubernetes 1.19+ or Docker 19.03+ (for containerized deployment)

### Kubernetes Deployment

The LLM Gateway is designed to run in Kubernetes. Here's a sample deployment configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-gateway
  namespace: aisera
spec:
  replicas: 2
  selector:
    matchLabels:
      app: llm-gateway
  template:
    metadata:
      labels:
        app: llm-gateway
    spec:
      containers:
      - name: llm-gateway
        image: aisera/llm-gateway:latest
        ports:
        - containerPort: 8300
          name: http
        - containerPort: 9090
          name: grpc
        env:
        - name: aisera_datastores_sql_host
          value: "mariadb"
        - name: aisera_datastores_sql_port
          value: "3306"
        - name: aisera_datastores_sql_uri
          value: "jdbc:mariadb://mariadb:3306/"
        - name: aisera_io_objectstore_plugin
          value: "com.aisera.plugins.io.aws.S3Store"
        - name: aisera_rest_webserver_port
          value: "8300"
        - name: aisera_service_name
          value: "llm-gateway"
        - name: aisera_sql_aisera_user
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: username
        - name: aisera_sql_password
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        readinessProbe:
          httpGet:
            path: /healthz
            port: 8300
          initialDelaySeconds: 30
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8300
          initialDelaySeconds: 60
          periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: llm-gateway
  namespace: aisera
spec:
  selector:
    app: llm-gateway
  ports:
  - port: 8300
    targetPort: 8300
    name: http
  - port: 9090
    targetPort: 9090
    name: grpc
  type: ClusterIP
```

To deploy:

```bash
kubectl apply -f llm-gateway-deployment.yaml
```

### Docker Deployment

You can also run the LLM Gateway using Docker Compose:

```yaml
version: '3'
services:
  llm-gateway:
    image: aisera/llm-gateway:latest
    ports:
      - "8300:8300"
      - "9090:9090"
    environment:
      - aisera_datastores_sql_host=mariadb
      - aisera_datastores_sql_port=3306
      - aisera_datastores_sql_uri=jdbc:mariadb://mariadb:3306/
      - aisera_io_objectstore_plugin=com.aisera.plugins.io.aws.S3Store
      - aisera_rest_webserver_port=8300
      - aisera_service_name=llm-gateway
      - aisera_sql_aisera_user=aisera_user
      - aisera_sql_password=password
      - hibernate.use.default.host=true
    depends_on:
      - mariadb
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8300/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3

  mariadb:
    image: mariadb:10.6
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=aisera
      - MYSQL_USER=aisera_user
      - MYSQL_PASSWORD=password
    volumes:
      - mariadb_data:/var/lib/mysql

  redis:
    image: redis:6.2
    volumes:
      - redis_data:/data

volumes:
  mariadb_data:
  redis_data:
```

To deploy:

```bash
docker-compose up -d
```

### Standalone Deployment

For development or testing purposes, you can run the LLM Gateway as a standalone Java application:

```bash
export aisera_datastores_sql_host=localhost
export aisera_datastores_sql_port=3306
export aisera_datastores_sql_uri=jdbc:mariadb://localhost:3306/
export aisera_io_objectstore_plugin=com.aisera.plugins.io.aws.S3Store
export aisera_rest_webserver_port=8300
export aisera_service_name=llm-gateway
export aisera_sql_aisera_user=aisera_user
export aisera_sql_password=password
export hibernate.use.default.host=true

# Run with Gradle
./gradlew run

# Or run with Java
java -jar llm-gateway.jar
```

## Configuration

### Environment Variables

The LLM Gateway is configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| aisera_datastores_sql_host | Database host | localhost |
| aisera_datastores_sql_port | Database port | 3306 |
| aisera_datastores_sql_uri | JDBC URI for the database | jdbc:mariadb://localhost:3306/ |
| aisera_io_objectstore_plugin | Object store plugin class | com.aisera.plugins.io.aws.S3Store |
| aisera_rest_webserver_port | REST server port | 8300 |
| aisera_service_name | Service name | llm-gateway |
| aisera_sql_aisera_user | Database username | - |
| aisera_sql_password | Database password | - |
| hibernate.use.default.host | Use default host for Hibernate | true |
| aisera_open_llm_url | URL for internal LLM service | - |
| cache | Cache type (local, redis) | local |
| OTEL_JAVAAGENT_ENABLED | Enable OpenTelemetry agent | false |

### Service Properties

Additional configuration can be provided in the `service.properties` file:

```properties
# Server configuration
server.port=8300
server.grpc.port=9090

# Database configuration
hibernate.dialect=org.hibernate.dialect.MariaDBDialect
hibernate.show_sql=false
hibernate.format_sql=false
hibernate.hbm2ddl.auto=update

# Cache configuration
cache.type=redis
cache.redis.host=redis
cache.redis.port=6379
cache.ttl.seconds=3600

# Metrics configuration
metrics.enabled=true
metrics.prometheus.port=8301

# LLM configuration
llm.default.max_retries=3
llm.default.timeout=30000
```

### Logging Configuration

The LLM Gateway uses Logback for logging. The configuration is in `logback.xml`:

```xml
<configuration>
  <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
      <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
    </encoder>
  </appender>

  <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>logs/llm-gateway.log</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>logs/llm-gateway.%d{yyyy-MM-dd}.log</fileNamePattern>
      <maxHistory>30</maxHistory>
    </rollingPolicy>
    <encoder>
      <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
    </encoder>
  </appender>

  <root level="INFO">
    <appender-ref ref="STDOUT" />
    <appender-ref ref="FILE" />
  </root>

  <logger name="com.aisera.service.llm" level="INFO" />
</configuration>
```

### Metrics Configuration

The LLM Gateway exposes metrics using Micrometer and Prometheus. The following metrics are available:

- `llm_tenant_execution_count`: Count of LLM executions by tenant, prompt, and LLM provider
- `llm_tenant_execution_latency_ms`: Latency of LLM executions
- `llm_tenant_cache_hits`: Cache hit count
- `llm_tenant_cache_misses`: Cache miss count
- `llm_tenant_cache_get_latency_ms`: Latency of cache get operations
- `llm_tenant_cache_put_latency_ms`: Latency of cache put operations
- `invocation_response_time_hist`: Histogram of invocation response times

## Scaling

### Horizontal Scaling

The LLM Gateway is designed to scale horizontally. You can deploy multiple instances behind a load balancer:

1. Increase the number of replicas in the Kubernetes deployment:
   ```yaml
   spec:
     replicas: 4
   ```

2. Use a horizontal pod autoscaler (HPA) to automatically scale based on CPU or memory usage:
   ```yaml
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: llm-gateway-hpa
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: llm-gateway
     minReplicas: 2
     maxReplicas: 10
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70
   ```

### Vertical Scaling

You can also scale the LLM Gateway vertically by increasing the resources allocated to each instance:

```yaml
resources:
  requests:
    memory: "4Gi"
    cpu: "2"
  limits:
    memory: "8Gi"
    cpu: "4"
```

### Resource Recommendations

| Traffic Level | Instances | CPU per Instance | Memory per Instance |
|---------------|-----------|------------------|---------------------|
| Low (<100 req/min) | 2 | 1 CPU | 2Gi |
| Medium (100-500 req/min) | 3-5 | 2 CPU | 4Gi |
| High (500-1000 req/min) | 5-8 | 4 CPU | 8Gi |
| Very High (>1000 req/min) | 8+ | 4+ CPU | 8Gi+ |

## Monitoring

### Health Checks

The LLM Gateway provides health check endpoints that can be used to monitor the service:

- **Readiness Check**: `/healthz` - Checks if the service is ready to accept requests
- **Liveness Check**: `/healthz/live` - Checks if the service is running
- **Database Check**: `/healthz/db` - Checks database connectivity
- **LLM Provider Check**: `/healthz/llm` - Checks LLM provider connectivity

### Metrics

Metrics are exposed via Prometheus at the `/metrics` endpoint on port 8301. You can configure Prometheus to scrape these metrics:

```yaml
scrape_configs:
  - job_name: 'llm-gateway'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        regex: llm-gateway
        action: keep
    metrics_path: /metrics
    scheme: http
```

### Logs

Logs are output to the console and to the `logs/llm-gateway.log` file. In a containerized environment, logs are output to stdout and can be collected by a logging system like Fluentd, Logstash, or Loki.

Important log messages to monitor:

- `ERROR` level messages - Indicate errors that require attention
- `WARN` level messages - Indicate potential issues that may need investigation
- Log messages containing "Exception" or "Error" - Indicate runtime exceptions

### Alerts

Configure the following alerts to monitor the health of the LLM Gateway:

1. **High Error Rate**:
   ```
   sum(rate(llm_tenant_execution_count{status="error"}[5m])) / sum(rate(llm_tenant_execution_count[5m])) > 0.05
   ```

2. **High Latency**:
   ```
   histogram_quantile(0.95, sum(rate(invocation_response_time_hist_bucket[5m])) by (le, instance)) > 5000
   ```

3. **Service Unavailable**:
   ```
   up{job="llm-gateway"} == 0
   ```

4. **High Cache Miss Rate**:
   ```
   sum(rate(llm_tenant_cache_misses[5m])) / (sum(rate(llm_tenant_cache_hits[5m])) + sum(rate(llm_tenant_cache_misses[5m]))) > 0.8
   ```

## Troubleshooting

### Common Issues

#### Database Connection Issues

Problem: The service fails to start with database connection errors.

Solution:
1. Check database credentials in environment variables.
2. Verify that the database server is running and accessible.
3. Check network connectivity between the LLM Gateway and the database.

#### LLM Provider Connection Issues

Problem: Requests to LLM providers fail with connection errors.

Solution:
1. Check LLM provider endpoint URLs in the configuration.
2. Verify API keys and credentials for the LLM providers.
3. Check network connectivity between the LLM Gateway and the LLM providers.
4. Look for rate limiting or quota issues with the LLM provider.

#### High Latency

Problem: Requests to the LLM Gateway are taking a long time to complete.

Solution:
1. Check the latency to the LLM providers.
2. Enable or optimize caching for frequently requested prompts.
3. Scale up the LLM Gateway instances.
4. Monitor database performance and optimize queries if needed.

#### Memory Issues

Problem: The service is experiencing out-of-memory errors.

Solution:
1. Increase the memory allocation for the service.
2. Check for memory leaks in the application.
3. Optimize request handling to reduce memory usage.
4. Tune the JVM garbage collection parameters.

### Debugging Tools

#### Enable Debug Logging

To enable more detailed logging, set the log level to DEBUG:

```xml
<logger name="com.aisera.service.llm" level="DEBUG" />
```

#### Debug Mode

Enable debug mode for API requests to get additional information:

```json
{
  "tenantId": "1000",
  "promptName": "example-prompt",
  "requestParams": [...],
  "config": {...},
  "isDebug": true
}
```

This will include detailed debug information in the response, including the applied template, request parameters, and timing information.

#### JVM Profiling

Use JVM profiling tools to diagnose performance issues:

```bash
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 -jar llm-gateway.jar
```

Then connect with a profiler like VisualVM, JProfiler, or YourKit.

### Support

For additional support, contact the Aisera Support team at support@aisera.com or open an issue in the internal issue tracker.