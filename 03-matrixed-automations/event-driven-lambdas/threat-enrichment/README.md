# Threat Intelligence Enrichment Pipeline (Pulumi YAML)

This pattern demonstrates a high-throughput, fault-tolerant threat indicator enrichment architecture.

## Architecture Highlights
- **SQS FIFO Ingestion Queue**: Enforces strict ordering and deduplication (`contentBasedDeduplication: true`) for indicator ingestion.
- **Dead-Letter Queue (DLQ) Safeguard**: Unprocessable messages automatically redirect to a DLQ after 3 failed delivery attempts with a 14-day retention window.
- **Batch Processing**: Lambda processes messages in batches of 10 with a 15-second batching window, drastically lowering invocation costs while maintaining low triage latency.
