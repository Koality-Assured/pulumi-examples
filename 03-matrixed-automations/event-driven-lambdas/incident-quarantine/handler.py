"""Incident response automated quarantine handler.

Receives high-severity compromise findings from EventBridge, extracts compromised
EC2 instance identifiers, creates a forensic disk snapshot, and attaches an
isolation security group to sever active network connections.
"""

import json
import logging
import os
import boto3
from typing import Dict, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ISOLATION_SG_ID = os.environ.get("ISOLATION_SG_ID", "")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Automated containment execution logic."""
    logger.info("Received security finding event: %s", json.dumps(event))

    detail = event.get("detail", {})
    resource_info = detail.get("resource", {})
    instance_details = resource_info.get("instanceDetails", {})
    instance_id = instance_details.get("instanceId")

    if not instance_id:
        logger.warning("Event does not contain an EC2 instance target. Skipping containment.")
        return {"statusCode": 200, "action": "ignored"}

    logger.warning("Initiating immediate automated quarantine for instance: %s", instance_id)

    ec2 = boto3.client("ec2")

    # Step 1: Snapshot root volumes for forensic analysis
    try:
        instance_desc = ec2.describe_instances(InstanceIds=[instance_id])
        reservations = instance_desc.get("Reservations", [])
        if reservations and reservations[0]["Instances"]:
            target_inst = reservations[0]["Instances"][0]
            for bdm in target_inst.get("BlockDeviceMappings", []):
                vol_id = bdm.get("Ebs", {}).get("VolumeId")
                if vol_id:
                    ec2.create_snapshot(
                        VolumeId=vol_id,
                        Description=f"Forensic snapshot of {vol_id} during automated quarantine of {instance_id}",
                        TagSpecifications=[
                            {
                                "ResourceType": "snapshot",
                                "Tags": [
                                    {"Key": "ForensicCapture", "Value": "True"},
                                    {"Key": "IncidentTarget", "Value": instance_id},
                                ],
                            }
                        ],
                    )
                    logger.info("Created forensic snapshot for volume %s", vol_id)

            # Step 2: Swap security groups to isolation SG
            if ISOLATION_SG_ID:
                for eni in target_inst.get("NetworkInterfaces", []):
                    eni_id = eni.get("NetworkInterfaceId")
                    ec2.modify_network_interface_attribute(
                        NetworkInterfaceId=eni_id,
                        Groups=[ISOLATION_SG_ID],
                    )
                    logger.warning("Attached isolation security group %s to ENI %s", ISOLATION_SG_ID, eni_id)

    except Exception as err:
        logger.error("Failed executing automated containment on %s: %s", instance_id, str(err))
        raise

    return {
        "statusCode": 200,
        "action": "quarantined",
        "instanceId": instance_id,
    }
