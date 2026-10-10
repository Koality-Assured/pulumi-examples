"""Matrix configuration parameters defining environment tiers and region deployments."""

from typing import Dict, Any, List

ENVIRONMENTS: List[str] = ["dev", "staging", "prod"]

REGIONS: Dict[str, str] = {
    "usw2": "us-west-2",
    "use1": "us-east-1",
    "euw1": "eu-west-1",
}

# Environment-specific configuration matrix
ENVIRONMENT_CONFIG: Dict[str, Dict[str, Any]] = {
    "dev": {
        "log_retention_days": 14,
        "enable_nat_gateway": False, # Cost saving in dev
        "vpc_cidr_prefix": "10.10",
    },
    "staging": {
        "log_retention_days": 30,
        "enable_nat_gateway": True,
        "vpc_cidr_prefix": "10.20",
    },
    "prod": {
        "log_retention_days": 365,
        "enable_nat_gateway": True,
        "vpc_cidr_prefix": "10.30",
    },
}

# Regional offset helper to ensure non-overlapping CIDR blocks
REGION_OCTET_OFFSET: Dict[str, int] = {
    "usw2": 0,
    "use1": 64,
    "euw1": 128,
}
