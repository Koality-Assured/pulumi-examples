"""Datadog Observability as Code using Pulumi Python.

Provisions automated alert monitors, weekly scheduled maintenance downtime
windows, and synthetic API health tests.
"""

import pulumi
import pulumi_datadog as datadog

config = pulumi.Config()
env = config.get("environment") or "production"
service_name = config.get("serviceName") or "platform-api"

# 1. Metric Alert Monitor: P99 Latency SLA Violation
p99_latency_monitor = datadog.Monitor(
    "api-p99-latency-monitor",
    name=f"[{env.upper()}] {service_name} - High P99 Latency (> 500ms)",
    type="metric alert",
    query=f"avg(last_5m):p99:trace.http.request.duration{{env:{env},service:{service_name}}} > 0.5",
    message=(
        f"P99 latency for {service_name} in {env} has exceeded 500ms over the last 5 minutes. "
        f"@slack-alerts-platform @pagerduty-{service_name}"
    ),
    tags=[
        f"env:{env}",
        f"service:{service_name}",
        "team:platform",
        "severity:p2",
    ],
    priority=2,
    notify_no_data=True,
    no_data_timeframe=10,
    renotify_interval=60,
    monitor_thresholds=datadog.MonitorMonitorThresholdsArgs(
        critical=0.5,
        warning=0.3,
    ),
)

# 2. Metric Alert Monitor: 5xx Error Rate Spike
error_rate_monitor = datadog.Monitor(
    "api-5xx-error-rate-monitor",
    name=f"[{env.upper()}] {service_name} - 5xx Error Rate Spike (> 2%)",
    type="metric alert",
    query=(
        f"sum(last_5m):sum:trace.http.request.errors{{env:{env},service:{service_name}}}.as_count() / "
        f"sum:trace.http.request.hits{{env:{env},service:{service_name}}}.as_count() > 0.02"
    ),
    message=(
        f"High 5xx error rate detected for {service_name} in {env}. Immediate investigation required. "
        f"@pagerduty-high-urgency"
    ),
    tags=[
        f"env:{env}",
        f"service:{service_name}",
        "team:platform",
        "severity:p1",
    ],
    priority=1,
    monitor_thresholds=datadog.MonitorMonitorThresholdsArgs(
        critical=0.02,
        warning=0.01,
    ),
)

# 3. Scheduled Maintenance Window (Weekly Sunday 02:00-04:00 UTC)
weekly_maintenance_downtime = datadog.DowntimeSchedule(
    "weekly-maintenance-downtime",
    scope=f"env:{env} AND service:{service_name}",
    recurring_schedule=datadog.DowntimeScheduleRecurringScheduleArgs(
        recurrences=[
            datadog.DowntimeScheduleRecurringScheduleRecurrenceArgs(
                duration="2h",
                rrule="FREQ=WEEKLY;BYDAY=SU",
                start="02:00",
            )
        ],
        timezone="UTC",
    ),
    display_timezone="UTC",
    message=f"Scheduled weekly maintenance window for {service_name} in {env}.",
    mute_first_recovery_notification=True,
)

# 4. Synthetic API Health Check (Every 1 Minute)
synthetic_health_check = datadog.SyntheticsTest(
    "api-health-synthetic-test",
    name=f"[{env.upper()}] {service_name} Health Endpoint Synthetic",
    type="api",
    subtype="http",
    status="live",
    request_definition=datadog.SyntheticsTestRequestDefinitionArgs(
        method="GET",
        url=f"https://{service_name}.example.com/healthz",
        timeout=10.0,
    ),
    request_headers={
        "User-Agent": "Datadog-Synthetic-HealthCheck",
    },
    assertions=[
        datadog.SyntheticsTestAssertionArgs(
            type="statusCode",
            operator="is",
            target=200,
        ),
        datadog.SyntheticsTestAssertionArgs(
            type="responseTime",
            operator="lessThan",
            target=500,
        ),
    ],
    locations=["aws:us-west-2", "aws:us-east-1", "aws:eu-west-1"],
    options_list=datadog.SyntheticsTestOptionsListArgs(
        tick_every=60,
        min_failure_duration=0,
        min_location_failed=2,
    ),
    message=f"Synthetic check failed for {service_name} in {env}. @slack-alerts-platform",
    tags=[f"env:{env}", f"service:{service_name}", "team:platform"],
)

# Export monitor IDs and ARNs
pulumi.export("p99LatencyMonitorId", p99_latency_monitor.id)
pulumi.export("errorRateMonitorId", error_rate_monitor.id)
pulumi.export("syntheticTestId", synthetic_health_check.id)
