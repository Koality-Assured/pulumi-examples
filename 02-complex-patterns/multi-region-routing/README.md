# Multi-Region Failover Routing (Pulumi YAML)

This pattern demonstrates configuring active-passive multi-region disaster recovery routing with Amazon Route53.

## Architectural Highlights
- **Automated Health Checks**: Route53 probes `/healthz` over HTTPS on the primary region (`us-east-1`) every 30 seconds.
- **Sub-Minute DNS Cutover**: Uses a low 60-second TTL on A records combined with `failoverRoutingPolicies`.
- **Zero-Downtime Resilience**: If the primary region fails 3 consecutive health checks, Route53 automatically strips the primary IP from DNS responses and directs all new client resolution to the secondary standby region (`us-west-2`).
