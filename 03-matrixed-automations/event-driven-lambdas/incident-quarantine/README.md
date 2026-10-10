# Incident Quarantine Automation (Pulumi YAML)

This pattern provisions an event-driven automated containment pipeline responding to high-severity Amazon GuardDuty findings.

## Containment Workflow
1. **EventBridge Ingestion**: Evaluates GuardDuty findings in real time, filtering for findings with severity >= 7.0 (high/critical compromise indicators).
2. **Forensic Preservation**: Before altering instance state, the Lambda takes snapshots of all attached EBS volumes with forensic preservation metadata tags.
3. **Network Isolation**: Replaces existing security groups on all instance Elastic Network Interfaces (ENIs) with an empty isolation security group (`ingress: []`, `egress: []`), instantly severing Command and Control (C2) communication without powering down the VM (preserving volatile RAM).
