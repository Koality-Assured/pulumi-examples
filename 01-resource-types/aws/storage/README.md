# Hardened AWS S3 Storage (Pulumi YAML)

This example provisions a high-security Amazon S3 bucket conforming to CIS AWS Foundations Benchmark standards.

## Security Baseline Controls
1. **Zero Public Access**: Attaches `aws:s3:BucketPublicAccessBlock` with all four flags enabled (`blockPublicAcls`, `blockPublicPolicy`, `ignorePublicAcls`, `restrictPublicBuckets`).
2. **KMS CMK Encryption & Bucket Keys**: Enforces AWS Key Management Service Customer Managed Key (`aws:kms`) encryption at rest, enabling `bucketKeyEnabled: true` to reduce KMS API costs by up to 99%.
3. **Mandatory TLS 1.2+ Transport**: An explicit `Deny` policy rejects any request initiated over plaintext HTTP (`aws:SecureTransport: false`) or using TLS versions older than 1.2 (`s3:TlsVersion < 1.2`).
4. **Versioning & Lifecycle Management**: Prevents accidental deletion or ransomware overwrites with object versioning, while auto-archiving noncurrent versions to Glacier after 90 days.
