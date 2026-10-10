# Multi-Environment Matrix Orchestration (Pulumi Python)

This example demonstrates how to leverage general-purpose programming languages (Python) to eliminate boilerplate when managing matrixed, multi-region cloud footprints.

## Key Capabilities
- **Explicit Multi-Region Providers (`aws.Provider`)**: Dynamically spins up dedicated AWS provider instances for each target region (`us-west-2`, `us-east-1`, `eu-west-1`), passing `opts=pulumi.ResourceOptions(provider=provider)` to resources.
- **Dynamic CIDR Math**: Calculates non-overlapping network subnets algorithmically based on environment tier (`dev`, `staging`, `prod`) and region octet offsets, eliminating IP collisions across peering connections.
- **Environment Policy Variations**: Automatically adjusts operational parameters (such as CloudWatch log retention periods and NAT Gateway enablement) based on environment criticality.
- **Strict Tag Governance**: Enforces standardized metadata propagation across all dynamically provisioned resources.
