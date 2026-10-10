# Pulumi-Managing-Pulumi (Pulumi Python)

This pattern demonstrates "meta-infrastructure" management: using the Pulumi Service Provider (`pulumi-pulumiservice`) to manage Pulumi Cloud teams, RBAC permissions, and ESC (Environments, Secrets, and Configuration) as code.

## Architecture Highlights
- **Declarative Organization Model**: The entire team-to-project hierarchy is declared in a Python data structure (`organization_model.py`), decoupling organizational policy from resource instantiation.
- **Granular RBAC Permissions (`pulumiservice.TeamStackPermission`)**: Automatically loops through teams and projects, provisioning exact stack permission levels (`admin`, `edit`, `read`) across environments.
- **Pulumi ESC with OIDC AWS Login**: Dynamically generates Pulumi ESC environments incorporating `fn::open::aws-login`. When developers or CI runners open an ESC environment, Pulumi automatically assumes an IAM role via OIDC and exports temporary AWS session tokens directly into environment variables.
