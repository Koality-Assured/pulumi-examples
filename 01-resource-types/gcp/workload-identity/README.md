# GCP Workload Identity Federation (Pulumi YAML)

This example configures keyless authentication between GitHub Actions and Google Cloud Platform using Workload Identity Federation (WIF).

## Why Workload Identity Federation?
Storing service account JSON keys in CI/CD secrets violates modern security baselines. Service account keys are non-expiring credentials that present severe exfiltration risks. WIF allows GitHub Actions workflows to exchange short-lived OIDC tokens for ephemeral GCP access tokens without persisting any long-lived secret keys.

## Architecture Highlights
- **OIDC Provider Mapping**: Maps GitHub's JWT claims (`sub`, `actor`, `repository`, `repository_owner`) into Google Security Token Service (STS) attributes.
- **Provider Assertion Conditions**: Enforces `assertion.repository_owner == 'koality-assured'` at the token exchange boundary, rejecting authentication attempts from unauthorized GitHub forks.
- **Workload Identity User Role**: Binds the principal set directly to `roles/iam.workloadIdentityUser` on the designated service account.
