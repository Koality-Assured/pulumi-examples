# AWS Networking Foundation (Pulumi YAML)

This example provisions a secure, multi-tier AWS VPC network topology using the native Pulumi YAML runtime.

## Architecture Highlights
- **VPC Isolation**: Dedicated `/16` IPv4 CIDR block with DNS hostnames and resolution enabled.
- **Tiered Subnets**: Segregated public subnet (`/24`) for load balancers/NAT gateways and private subnet (`/24`) for backend compute and databases.
- **Controlled Egress**: Private workloads reach external internet endpoints via an AWS Managed NAT Gateway backed by an Elastic IP. Direct public IP assignment on launch is explicitly disabled (`mapPublicIpOnLaunch: false`).
- **Least-Privilege Security Group**: Restricts inbound traffic to internal TLS (`443`) and constrains egress to encrypted endpoints.

## Exported Outputs
This stack exports foundational identifiers for downstream stacks (such as compute, databases, or load balancers) to ingest via `StackReference`:
- `vpcId`: VPC identifier.
- `publicSubnetId`: Identifier for public subnet tier.
- `privateSubnetId`: Identifier for private subnet tier.
- `appSecurityGroupId`: Base security group for app workloads.
