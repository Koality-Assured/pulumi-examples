# Domain 01: Resource Types

This directory provides isolated, production-grade examples demonstrating how to deploy foundational cloud and SaaS resources successfully using Pulumi.

## Navigation Matrix

| Provider | Area | Runtime | Focus & Key Capabilities | Directory |
| :--- | :--- | :--- | :--- | :--- |
| **AWS** | Networking | Pulumi YAML | VPC, public/private subnets, NAT Gateway, EIP, Route Tables, App Security Groups | [`aws/networking/`](./aws/networking/) |
| **AWS** | Compute | Pulumi YAML | EC2 instances, Ubuntu AMI lookup (`fn::invoke`), KMS CMK root volume encryption, IMDSv2 enforcement, SSM instance profile | [`aws/compute/`](./aws/compute/) |
| **AWS** | Load Balancing | Pulumi YAML | Application Load Balancer (ALB), target groups, health checks, HTTPS listener (TLS 1.3), HTTP-to-HTTPS redirect | [`aws/loadbalancing/`](./aws/loadbalancing/) |
| **AWS** | API Gateway | Pulumi YAML | REST API v1, resource trees (`/api/v1/health`), mock integration, deployment stage | [`aws/apigateway/`](./aws/apigateway/) |
| **AWS** | Storage | Pulumi YAML | Hardened S3 bucket, KMS CMK encryption, S3 Public Access Block (all 4 vectors), TLS 1.2+ enforce bucket policy, lifecycle rules | [`aws/storage/`](./aws/storage/) |
| **AWS** | Identity | Pulumi YAML | IAM OIDC Identity Provider for GitHub Actions, scoped trust boundary, least-privilege deployment policy | [`aws/identity/`](./aws/identity/) |
| **AWS** | Edge | Pulumi YAML | CloudFront CDN distribution, origin failover groups (HTTP 5xx failover), WAFv2 WebACL with AWS Managed Rules and IP rate limiting, SPA routing | [`aws/edge/`](./aws/edge/) |
| **GCP** | Identity | Pulumi YAML | Workload Identity Federation (WIF) with GitHub Actions OIDC, attribute conditions, keyless service account token creation | [`gcp/workload-identity/`](./gcp/workload-identity/) |
| **GCP** | Networking | Pulumi YAML | Regional SSL Policy (`RegionSslPolicy`) with `RESTRICTED` profile and `TLS_1_2` minimum version | [`gcp/security-policies/`](./gcp/security-policies/) |
| **Linode** | Multi-Cloud | Pulumi YAML | Independent VM provisioning, private datacenter networking, Cloud Firewall with default DROP and rate/port limits, scoped API tokens | [`linode/compute-and-firewall/`](./linode/compute-and-firewall/) |
| **SaaS** | GitHub Org | Pulumi YAML | GitHub Organization-as-Code: teams, repository templates with secret scanning enabled, branch protections, RBAC grants | [`saas/github-org/`](./saas/github-org/) |
| **SaaS** | Datadog | Pulumi Python | Observability-as-Code: P99 latency alerts, 5xx error rate anomaly monitors, weekly scheduled maintenance downtime windows, synthetic tests | [`saas/datadog-monitoring/`](./saas/datadog-monitoring/) |
