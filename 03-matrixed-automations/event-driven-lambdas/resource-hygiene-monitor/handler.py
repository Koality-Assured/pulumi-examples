"""Scheduled cloud hygiene scanner Lambda handler.

Identifies orphaned AWS resources (unattached EBS volumes, unassociated Elastic IPs)
and generates FinOps optimization alerts.
"""

import json
import logging
import os
import boto3
from typing import Dict, Any, List

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")


def scan_unattached_volumes(ec2_client: Any) -> List[Dict[str, Any]]:
    """Identifies EBS volumes in 'available' status not mounted to any instance."""
    orphans = []
    paginator = ec2_client.get_paginator("describe_volumes")
    for page in paginator.paginate(Filters=[{"Name": "status", "Values": ["available"]}]):
        for vol in page.get("Volumes", []):
            orphans.append({
                "volume_id": vol["VolumeId"],
                "size_gib": vol["Size"],
                "volume_type": vol["VolumeType"],
                "create_time": str(vol["CreateTime"]),
            })
    return orphans


def scan_unassociated_addresses(ec2_client: Any) -> List[Dict[str, Any]]:
    """Identifies allocated Elastic IPs not associated with any network interface or instance."""
    unassociated = []
    response = ec2_client.describe_addresses()
    for addr in response.get("Addresses", []):
        if "AssociationId" not in addr and "InstanceId" not in addr:
            unassociated.append({
                "public_ip": addr.get("PublicIp"),
                "allocation_id": addr.get("AllocationId"),
            })
    return unassociated


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Scheduled execution logic for cloud waste scanning."""
    logger.info("Executing scheduled cloud hygiene sweep...")

    ec2 = boto3.client("ec2")

    unattached_vols = scan_unattached_volumes(ec2)
    unassociated_ips = scan_unassociated_addresses(ec2)

    logger.info("Found %d unattached EBS volumes", len(unattached_vols))
    logger.info("Found %d unassociated Elastic IPs", len(unassociated_ips))

    report = {
        "unattached_volumes_count": len(unattached_vols),
        "unassociated_ips_count": len(unassociated_ips),
        "unattached_volumes": unattached_vols,
        "unassociated_ips": unassociated_ips,
    }

    return {
        "statusCode": 200,
        "report": report,
    }
