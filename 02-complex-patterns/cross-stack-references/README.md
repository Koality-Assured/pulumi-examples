# Complex Pattern: Cross-Stack References

This pattern demonstrates decomposing enterprise cloud architecture into decoupled, autonomous micro-stacks using Pulumi's native `StackReference` capability.

```
┌─────────────────────────────────┐
│   pattern-cross-stack-network   │
│   (VPC, Subnets, Gateways)      │
└────────────────┬────────────────┘
                 │ Exports: vpcId, subnetIds
                 ▼
┌─────────────────────────────────┐
│     pattern-cross-stack-app     │
│   (Compute, Security Groups)    │
└─────────────────────────────────┘
```

## Architectural Benefits
1. **Decoupled Blast Radius**: Network modifications or routing updates cannot accidentally trigger destructive replacements of application servers or databases.
2. **Independent Lifecycles**: Application developers can iterate rapidly on application tiers without possessing mutating permissions on shared VPC networking infrastructure.
3. **Formal State Contracts**: Outputs define a typed public contract. Internal implementation changes inside the network stack do not impact downstream consumers as long as the exported schema remains stable.
