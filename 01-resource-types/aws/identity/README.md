# AWS Identity & OIDC Integration (Pulumi YAML)

This example establishes keyless, credential-free authentication for CI/CD pipelines using AWS OpenID Connect (OIDC) identity federation.

## Why Keyless OIDC?
Long-lived AWS access keys (`AKIA...`) stored in CI/CD secrets present significant security hazards (credential exfiltration, lack of rotation, privilege creep). OIDC federation exchanges short-lived JSON Web Tokens (JWTs) issued by GitHub Actions for ephemeral AWS STS credentials.

## Security Highlights
- **Scoped Trust Boundary**: The `assumeRolePolicy` asserts both `aud == sts.amazonaws.com` and a restrictive `sub` claim matching only repositories within the designated organization (`repo:koality-assured/*:*`).
- **Bounded Session Duration**: Restricts role assumption duration to 3,600 seconds (1 hour) to limit the blast radius of temporary tokens.
- **Granular Least Privilege**: Replaces permissive administrator access with explicit service permissions for state manipulation and inspection.
