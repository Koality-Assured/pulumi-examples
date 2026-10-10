# Spoke Account Onboarding Bootstrap

This template is deployed into workload (spoke) AWS accounts to link them into the centralized Systems Manager platform.

## Resources Bootstrapped
1. **`SpokeExecutionRole`**: An IAM role allowing the central governance operator role (`arn:aws:iam::123456789012:role/role-central-ssm-operator`) to run automation documents, run commands, and trigger maintenance windows across member accounts.
2. **`ManagedInstanceProfile`**: Standardized IAM instance profile for application VMs that enables SSM Agent connectivity and CloudWatch metrics collection without requiring SSH keys or inbound firewall openings.
3. **Cross-Account EventBridge Rule**: Streams SSM compliance state transitions, patch run outcomes, and instance status changes in real time directly to the central governance EventBridge bus.
