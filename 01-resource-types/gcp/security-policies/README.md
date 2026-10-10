# GCP Regional SSL Policy (Pulumi YAML)

This example provisions an enterprise SSL security policy for Google Cloud Load Balancing infrastructure using Pulumi YAML.

## Security Highlights
- **Strict Cipher Suite Profile (`profile: RESTRICTED`)**: Restricts negotiated cipher suites to high-strength algorithms, disabling legacy and vulnerable cipher configurations (such as RC4, 3DES, or static CBC ciphers).
- **Minimum TLS Version (`minTlsVersion: TLS_1_2`)**: Rejects outdated TLS 1.0 and TLS 1.1 handshake negotiations, ensuring compliance with modern security and data privacy mandates (PCI-DSS, HIPAA, NIST CSF).
- **Regional Deployment**: Applies directly to regional Google Cloud Target HTTPS Proxies in the specified deployment region (`us-west1`).
