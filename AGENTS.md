# Repository AGENTS

Canonical rules for AI agents operating within `Koality-Assured/pulumi-examples`.

## Scope & Purpose
This repository provides production-grade, generalized, secure Infrastructure as Code (IaC) architectural patterns and resource examples using Pulumi (YAML, Python, and TypeScript Policy Packs). It serves as an authoritative reference for complex patterns, multi-resource provisioning, multi-cloud deployments (AWS, GCP, Linode), SaaS governance (GitHub, Datadog), and matrixed serverless automations.

## Non-Negotiable Directives

### 1. Sanitization & Public Hygiene (CRITICAL)
- **Zero Secrets / Internal Identifiers**: NEVER commit or hardcode private credentials, API keys, internal company names (e.g. legacy corporate entities, subsidiaries, proprietary code names), internal employee names, or real AWS/GCP account numbers.
- **Forbidden Identifier Check**: All code and documentation must strictly pass `adversarial_review.py` with zero forbidden terms.
- **Synthetic Placeholders**: Use obvious synthetic placeholders (`123456789012`, `example.com`, `sample-org`, `us-west-2a`, `arn:aws:iam::123456789012:role/SampleRole`).

### 2. Example-Only Scope (NO Real Execution)
- **No Live GitHub Actions**: Do NOT create real `.github/workflows/` runner pipelines that execute against cloud providers. CI/CD integration patterns must be documented in Markdown or sample non-executing templates.
- **No Live Pulumi Deployments**: Do NOT invoke `pulumi up` or mutate real cloud environments from this repository. All manifests and programs must be syntactically valid and structurally complete for reference and testing.

### 3. Progressive Navigation & Structure
- Examples are partitioned into three dedicated domains:
  1. `01-resource-types/` (AWS, GCP, Linode, SaaS)
  2. `02-complex-patterns/` (Cross-Stack, Hub-and-Spoke SSM, Route53 Failover, CrossGuard, Pulumi-Managing-Pulumi)
  3. `03-matrixed-automations/` (Multi-Environment Matrix, Serverless Event-Driven Lambdas)
- Every subdirectory must maintain an informative `README.md` explaining architecture, design tradeoffs, inputs, and outputs.

### 4. Adversarial Review Standard
- Before merging any branch into `main`, `python adversarial_review.py` must execute cleanly with zero warnings or failures.
