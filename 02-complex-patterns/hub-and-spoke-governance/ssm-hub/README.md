# Central Systems Manager (SSM) Governance Hub

This stack provisions central fleet governance and compliance tooling in a centralized management account.

## Architectural Highlights
- **Magic Document (`SSM-SessionManagerRunShell`)**: AWS Systems Manager applies inputs from a document with this exact name to every interactive shell session in the region. This example enforces:
  - Encryption in transit using a KMS Customer Managed Key.
  - Mandatory streaming of all terminal input/output into a designated CloudWatch Log Group.
  - Idle session timeout disconnected after 20 minutes.
- **Tiered Patch Baselines**:
  - `tier-critical`: 3-day approval window for high-criticality production instances.
  - `tier-standard`: 7-day approval window for lower-criticality and staging instances.
  - Instances pick up their baseline automatically via the `patch-group` tag (`aws:ssm:PatchGroup`).
- **Resource Data Sync**: Collects software inventory, OS patch compliance, and instance hardware metadata into a central S3 data lake for fleet-wide reporting.
