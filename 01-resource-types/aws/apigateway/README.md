# AWS API Gateway REST API (Pulumi YAML)

This example details how to declare a hierarchical REST API via AWS API Gateway v1 using Pulumi YAML.

## Architecture Highlights
- **Resource Tree**: Demonstrates building child paths using parent ID references (`rootResourceId` -> `/api` -> `/v1` -> `/health`).
- **Mock Integration**: Uses a serverless `MOCK` integration to return an immediate HTTP 200 health payload without dispatching backend compute, saving cost and reducing latency for liveness probes.
- **Explicit Deployment Order**: Utilizes Pulumi's `dependsOn` option to enforce that the `Deployment` resource captures all methods, resources, and integration responses before creating or updating the `Stage`.
