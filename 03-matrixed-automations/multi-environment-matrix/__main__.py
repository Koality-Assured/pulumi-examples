"""Programmatic infrastructure matrix automation in Pulumi Python.

Loops across [environments] x [regions], dynamically generating regional AWS
providers, isolated VPCs, subnets, and CloudWatch log groups with non-overlapping
CIDRs and strict tag inheritance.
"""

import pulumi
import pulumi_aws as aws
from matrix_config import (
    ENVIRONMENTS,
    REGIONS,
    ENVIRONMENT_CONFIG,
    REGION_OCTET_OFFSET,
)

# 1. Instantiate Regional Providers
regional_providers = {}
for reg_key, reg_name in REGIONS.items():
    regional_providers[reg_key] = aws.Provider(
        f"aws-provider-{reg_key}",
        region=reg_name,
    )

# 2. Programmatically Generate the Matrix
vpc_matrix_outputs = {}

for env in ENVIRONMENTS:
    env_cfg = ENVIRONMENT_CONFIG[env]
    retention_days = env_cfg["log_retention_days"]

    for reg_key, reg_name in REGIONS.items():
        provider = regional_providers[reg_key]
        offset = REGION_OCTET_OFFSET[reg_key]
        prefix = env_cfg["vpc_cidr_prefix"]
        vpc_cidr = f"{prefix}.{offset}.0/18"
        public_subnet_cidr = f"{prefix}.{offset}.10.0/24"

        matrix_slug = f"{env}-{reg_key}"

        # Standardized Tags
        standard_tags = {
            "Environment": env.capitalize(),
            "Region": reg_name,
            "ManagedBy": "PulumiMatrixAutomation",
            "MatrixCell": matrix_slug,
        }

        # Central Log Group for VPC Flow Logs
        flow_log_group = aws.cloudwatch.LogGroup(
            f"log-group-vpc-{matrix_slug}",
            name=f"/aws/vpc/flow-logs/{matrix_slug}",
            retention_in_days=retention_days,
            tags=standard_tags,
            opts=pulumi.ResourceOptions(provider=provider),
        )

        # Regional Isolated VPC
        vpc = aws.ec2.Vpc(
            f"vpc-{matrix_slug}",
            cidr_block=vpc_cidr,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            tags={**standard_tags, "Name": f"vpc-{matrix_slug}"},
            opts=pulumi.ResourceOptions(provider=provider),
        )

        # Regional Public Subnet
        subnet = aws.ec2.Subnet(
            f"snet-public-{matrix_slug}",
            vpc_id=vpc.id,
            cidr_block=public_subnet_cidr,
            map_public_ip_on_launch=False,
            tags={**standard_tags, "Name": f"snet-public-{matrix_slug}"},
            opts=pulumi.ResourceOptions(provider=provider),
        )

        vpc_matrix_outputs[matrix_slug] = {
            "vpc_id": vpc.id,
            "cidr": vpc_cidr,
            "subnet_id": subnet.id,
            "log_group_arn": flow_log_group.arn,
        }

# Export the matrix topology
pulumi.export("matrixDeployments", vpc_matrix_outputs)
