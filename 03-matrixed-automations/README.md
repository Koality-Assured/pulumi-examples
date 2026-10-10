# Domain 03: Matrixed Automations & Serverless Workflows

This directory showcases programmatic infrastructure automation patterns that reduce operational overhead across large-scale, multi-environment, and serverless architectures.

## Navigation Matrix

| Automation Area | Runtime | Focus & Capabilities | Directory |
| :--- | :--- | :--- | :--- |
| **Multi-Environment Matrix** | Pulumi Python | Matrix expansion across `[dev, staging, prod]` x `[regions]`: dynamically generates regional AWS providers, deterministic non-overlapping CIDRs, and tier-specific log retention | [`multi-environment-matrix/`](./multi-environment-matrix/) |
| **Threat Enrichment Pipeline** | Pulumi YAML / Python | Asynchronous threat intelligence enrichment: SQS FIFO queues with content-based deduplication, DLQ redrive policies, batching window, and serverless enrichment workers | [`event-driven-lambdas/threat-enrichment/`](./event-driven-lambdas/threat-enrichment/) |
| **Incident Quarantine Automation** | Pulumi YAML / Python | Automated incident containment: EventBridge rule capturing high-severity compromise findings, automated forensic snapshotting, and security group isolation | [`event-driven-lambdas/incident-quarantine/`](./event-driven-lambdas/incident-quarantine/) |
| **Resource Hygiene Monitor** | Pulumi YAML / Python | Scheduled FinOps sweeping: Daily EventBridge cron trigger invoking a serverless auditor that detects unattached EBS volumes and unassociated Elastic IPs | [`event-driven-lambdas/resource-hygiene-monitor/`](./event-driven-lambdas/resource-hygiene-monitor/) |
