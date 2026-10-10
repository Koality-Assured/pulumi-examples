"""Declarative data model defining the organization's Pulumi Cloud hierarchy."""

from typing import Dict, Any, List

ORG_NAME = "koality-assured"

TEAMS: List[Dict[str, str]] = [
    {"name": "platform-engineers", "description": "Core Cloud Platform & Infrastructure Team"},
    {"name": "security-engineers", "description": "Information Security & Compliance Team"},
    {"name": "application-developers", "description": "App Tier Developers and Microservice Teams"},
]

# Matrix of Team -> Projects -> Stacks
ORG_LAYOUT: Dict[str, Dict[str, Any]] = {
    "platform-engineers": {
        "core-networking": {
            "stacks": {"prod-usw2": "us-west-2", "prod-use1": "us-east-1"},
            "permission": "admin",
            "account_id": "123456789012",
        },
        "ssm-governance": {
            "stacks": {"hub-usw2": "us-west-2"},
            "permission": "admin",
            "account_id": "123456789012",
        },
    },
    "security-engineers": {
        "incident-response-lambdas": {
            "stacks": {"prod-usw2": "us-west-2"},
            "permission": "admin",
            "account_id": "222233334444",
        },
    },
    "application-developers": {
        "ecommerce-frontend": {
            "stacks": {"dev-usw2": "us-west-2", "prod-usw2": "us-west-2"},
            "permission": "edit",
            "account_id": "333344445555",
        },
    },
}

ESC_ACCOUNTS: List[Dict[str, str]] = [
    {
        "env_name": "aws-platform-prod",
        "account_id": "123456789012",
        "role_name": "role-pulumi-deployer",
    },
    {
        "env_name": "aws-secops-prod",
        "account_id": "222233334444",
        "role_name": "role-pulumi-deployer",
    },
]
