# Datadog Observability as Code (Pulumi Python)

This example provisions complete observability and alerting infrastructure using the Pulumi Datadog provider in Python.

## Components Configured
1. **P99 Latency SLA Violation Monitor**: Alerts when APM trace latency exceeds 500ms over a 5-minute rolling window with warning thresholds at 300ms.
2. **Error Rate Spike Monitor**: Tracks the ratio of HTTP errors to total hits, triggering high-severity alerts when the failure rate exceeds 2%.
3. **Recurring Maintenance Downtime**: Establishes an automated recurring weekly downtime window (Sundays 02:00-04:00 UTC) with notification suppression (`mute_first_recovery_notification: true`) to eliminate false alarms during scheduled deployments.
4. **Global Synthetic Health Check**: Probes the application `/healthz` endpoint once per minute from multiple global cloud vantage points (`us-west-2`, `us-east-1`, `eu-west-1`), failing only if two or more locations report degradation.
