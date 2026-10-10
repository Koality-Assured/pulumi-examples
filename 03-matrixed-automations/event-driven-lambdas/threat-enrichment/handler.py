"""Threat enrichment serverless worker.

Processes batches of file/IP indicators from SQS, enriches indicators against
threat intelligence feeds, and emits enriched telemetry for triage.
"""

import json
import logging
import os
from typing import Dict, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
FEED_ENDPOINT = os.environ.get("THREAT_FEED_ENDPOINT", "https://api.threatintel.example.com/v1")


def query_threat_intel(indicator: str, indicator_type: str) -> Dict[str, Any]:
    """Simulates querying external threat intelligence APIs (e.g. VirusTotal/AlienVault)."""
    # Generalized demonstration response
    return {
        "indicator": indicator,
        "type": indicator_type,
        "verdict": "suspicious" if len(indicator) % 2 == 0 else "benign",
        "reputation_score": 75 if len(indicator) % 2 == 0 else 10,
        "threat_families": ["Generic.Trojan.Downloader"] if len(indicator) % 2 == 0 else [],
        "enriched_at_utc": "2026-10-10T00:00:00Z",
    }


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AWS Lambda entry point processing SQS batch records."""
    records = event.get("Records", [])
    logger.info("Received batch of %d records for threat enrichment", len(records))

    processed_count = 0
    findings = []

    for record in records:
        try:
            body = json.loads(record["body"])
            indicator = body.get("indicator", "")
            indicator_type = body.get("type", "sha256")

            if not indicator:
                logger.warning("Skipping record with missing indicator: %s", record["messageId"])
                continue

            enrichment_result = query_threat_intel(indicator, indicator_type)
            findings.append(enrichment_result)
            processed_count += 1

            logger.info(
                "Enriched indicator: %s | Type: %s | Verdict: %s",
                indicator,
                indicator_type,
                enrichment_result["verdict"],
            )

        except Exception as err:
            logger.error("Error processing message %s: %s", record.get("messageId"), str(err))
            raise  # SQS redrive policy handles failed messages via DLQ

    return {
        "statusCode": 200,
        "processed_count": processed_count,
        "findings": findings,
    }
