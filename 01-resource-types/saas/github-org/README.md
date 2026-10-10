# GitHub Organization-as-Code (Pulumi YAML)

This example manages an entire GitHub enterprise organization declarative configuration using the Pulumi GitHub provider.

## Governance Highlights
- **Role-Based Access Control (RBAC)**: Defines engineering teams (`github:Team`) and maps granular repository permissions (`github:TeamRepository`) programmatically, avoiding manual permission drift.
- **Repository Security Defaults**: Enforces secret scanning and secret scanning push protection out of the box on newly created repository templates.
- **Comprehensive Branch Protection**: Mandates strict rules on default branches:
  - Required status checks (`strict: true`).
  - Required code owner approvals (`requireCodeOwnerReviews: true`).
  - GPG/SSH commit signature verification (`requireSignedCommits: true`).
  - Admin enforcement (`enforceAdmins: true`) to prevent bypasses.
  - Prohibition of force pushes and branch deletions.
