# Network Tier Micro-Stack

This stack provisions the core network boundary and exports stable infrastructure identifiers:
- `vpcId`
- `vpcCidr`
- `publicSubnetId`
- `privateSubnetId`

By decoupling networking into its own stack, network lifecycles (which change infrequently and carry catastrophic risk if deleted) are strictly separated from application tiers.
