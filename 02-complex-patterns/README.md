# Domain 02: Complex Architectural Patterns

This directory provides advanced architectural patterns for orchestrating complex enterprise cloud environments, cross-stack coordination, multi-account governance, and compliance-as-code.

## Navigation Matrix

| Pattern | Runtime | Focus & Capabilities | Directory |
| :--- | :--- | :--- | :--- |
| **Cross-Stack References** | Pulumi YAML | Decoupled micro-stacks: Network tier outputs consumed by App tier via `pulumi:pulumi:StackReference` | [`cross-stack-references/`](./cross-stack-references/) |
| **Hub-and-Spoke Governance** | Pulumi YAML / CloudFormation | Multi-account Systems Manager (SSM) hub with 2-tier patch baselines, magic session preferences (`SSM-SessionManagerRunShell`), Resource Data Sync, and spoke onboarding | [`hub-and-spoke-governance/`](./hub-and-spoke-governance/) |
| **Multi-Region Failover** | Pulumi YAML | Active-passive disaster recovery DNS routing via Amazon Route53 with automated HTTPS health probes and sub-minute cutover | [`multi-region-routing/`](./multi-region-routing/) |
| **Policy-as-Code** | TypeScript / CrossGuard | Pre-deployment compliance evaluation using Pulumi CrossGuard (`@pulumi/awsguard` + custom tagging, IMDSv2, and S3 encryption policies) | [`policy-as-code-crossguard/`](./policy-as-code-crossguard/) |
| **Pulumi-Managing-Pulumi** | Pulumi Python | Meta-infrastructure: Pulumi Service Provider (`pulumiservice`) managing teams, stack RBAC, and Pulumi ESC environments with AWS OIDC login | [`pulumi-managing-pulumi/`](./pulumi-managing-pulumi/) |
