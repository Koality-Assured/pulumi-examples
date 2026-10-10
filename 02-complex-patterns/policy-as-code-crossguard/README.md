# Policy-as-Code with Pulumi CrossGuard (TypeScript)

This directory defines an enterprise compliance Policy Pack using Pulumi CrossGuard.

## Enforcement Architecture
CrossGuard policies evaluate resource declarations **before** cloud API mutations take place. If a resource violates a `mandatory` policy, `pulumi preview` and `pulumi up` fail immediately with a detailed violation report.

## Policies Implemented
1. **AwsGuard (`@pulumi/awsguard`)**: Baseline CIS AWS compliance rules loaded in `advisory` mode.
2. **`require-standard-tags` (Mandatory)**: Validates that all taggable cloud resources include `Environment` and `Service` tags for FinOps tracking.
3. **`require-ec2-imdsv2` (Mandatory)**: Ensures all EC2 instances configure `httpTokens: "required"`, blocking IMDSv1 tokenless metadata access.
4. **`require-s3-encryption` (Mandatory)**: Prevents provisioning unencrypted S3 buckets.

## Testing Locally
```bash
pulumi preview --policy-pack ../policy-as-code-crossguard
```
