# Resource Hygiene & FinOps Monitor (Pulumi YAML)

This pattern provisions a scheduled serverless auditor that sweeps AWS accounts for orphaned, idle, and unattached cloud resources.

## Architecture Highlights
- **Scheduled Trigger**: Utilizes Amazon EventBridge to execute on a daily cron expression (`cron(0 6 * * ? *)`).
- **Orphan Detection**: Scans for unattached EBS storage volumes (status `available`) and unassociated Elastic IPs that incur ongoing hourly idle charges.
- **FinOps Optimization**: Generates structured reports suitable for delivery to Slack webhooks, SNS notification topics, or automated tag-and-reap cleanup workflows.
