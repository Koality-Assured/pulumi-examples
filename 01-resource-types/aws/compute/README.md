# AWS Compute Workload (Pulumi YAML)

This example illustrates deploying an enterprise-hardened EC2 workload in AWS using Pulumi YAML.

## Key Patterns Demonstrated
1. **Dynamic AMI Lookups (`fn::invoke: aws:ec2:getAmi`)**: Queries Canonical's official owner ID (`099720109477`) dynamically for the latest stable Ubuntu 22.04 LTS release, avoiding fragile hardcoded AMI IDs.
2. **IMDSv2 Enforcement**: Configures `metadataOptions` with `httpTokens: required` and `httpPutResponseHopLimit: 1` to neutralize Server-Side Request Forgery (SSRF) attack vectors against instance profile metadata.
3. **KMS CMK-Encrypted Storage**: Enforces hardware-backed encryption at rest for EBS root volumes via a Customer Managed Key (CMK) configured for annual key rotation.
4. **Zero-Inbound Bastionless Operations**: Attaches `AmazonSSMManagedInstanceCore` via an instance profile, allowing secure remote shell access and patching through AWS Systems Manager without opening SSH port 22 to any IP ranges.
5. **StackReference Integration**: Ingests subnet and security group IDs from the standalone networking stack via `pulumi:pulumi:StackReference`.
