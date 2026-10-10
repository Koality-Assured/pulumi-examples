# Complex Pattern: Hub-and-Spoke Governance

This pattern demonstrates an enterprise multi-account Systems Manager (SSM) governance architecture.

```
┌────────────────────────────────────────────────────────┐
│             Central Hub Account (123456789012)         │
│  - SSM-SessionManagerRunShell (CMK Encrypted + Logs)   │
│  - Multi-OS Patch Baselines (tier-critical/standard)   │
│  - Central Inventory Resource Data Sync S3 Lake        │
│  - Central EventBridge Compliance Event Bus            │
└───────────────────────────▲────────────────────────────┘
                            │ Cross-Account STS AssumeRole
                            │ & EventBridge Stream
            ┌───────────────┴───────────────┐
            │                               │
┌───────────┴───────────────┐   ┌───────────┴───────────────┐
│  Spoke Account A (Prod)   │   │  Spoke Account B (Dev)    │
│  - SpokeExecutionRole     │   │  - SpokeExecutionRole     │
│  - ManagedInstanceProfile │   │  - ManagedInstanceProfile │
│  - Event Forwarder Rule   │   │  - Event Forwarder Rule   │
└───────────────────────────┘   └───────────────────────────┘
```

## Problem Solved
Managing patch baselines, session security, and software inventory across hundreds of AWS accounts individually leads to configuration divergence and severe compliance gaps. This pattern standardizes:
1. One central session preference document applying encryption and log streaming to all terminal sessions.
2. Standardized patch baselines automatically resolved across OS families by tagging instances `patch-group=tier-critical`.
3. Event-driven compliance collection streaming patch states to a central event bus.
