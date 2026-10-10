"""Meta-infrastructure program managing Pulumi Cloud as Code.

Provisions teams, sets up stack permissions, and generates Pulumi ESC
(Environments, Secrets, and Configuration) definitions with OIDC authentication.
"""

import textwrap
import pulumi
import pulumi_pulumiservice as pulumiservice
from organization_model import ORG_NAME, TEAMS, ORG_LAYOUT, ESC_ACCOUNTS

# Permission mapping helper (admin=103, edit=102, read=101)
PERMISSION_MAP = {
    "admin": "admin",
    "edit": "edit",
    "read": "read",
}

# 1. Provision Teams
created_teams = {}
for team_def in TEAMS:
    team_name = team_def["name"]
    team = pulumiservice.Team(
        f"team-{team_name}",
        name=team_name,
        description=team_def["description"],
        organization_name=ORG_NAME,
    )
    created_teams[team_name] = team

# 2. Iterate Layout to Configure Team Stack Permissions
created_permissions = []
for team_name, projects in ORG_LAYOUT.items():
    team_resource = created_teams[team_name]
    for project_name, project_config in projects.items():
        perm_level = project_config.get("permission", "read")
        stacks = project_config.get("stacks", {})

        for stack_name, region in stacks.items():
            perm_id = f"perm-{team_name}-{project_name}-{stack_name}"
            permission = pulumiservice.TeamStackPermission(
                perm_id,
                organization_name=ORG_NAME,
                project_name=project_name,
                stack_name=stack_name,
                team_name=team_resource.name,
                permission=PERMISSION_MAP.get(perm_level, "read"),
            )
            created_permissions.append(permission)

# 3. Create Pulumi ESC Environments for Keyless Cloud Access
created_esc_envs = []
for esc_def in ESC_ACCOUNTS:
    env_name = esc_def["env_name"]
    account_id = esc_def["account_id"]
    role_name = esc_def["role_name"]
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"

    esc_yaml = textwrap.dedent(f"""\
        values:
          aws:
            login:
              fn::open::aws-login:
                oidc:
                  duration: 1h
                  roleArn: {role_arn}
                  sessionName: pulumi-esc-session
          environmentVariables:
            AWS_ACCESS_KEY_ID: ${{aws.login.accessKeyId}}
            AWS_SECRET_ACCESS_KEY: ${{aws.login.secretAccessKey}}
            AWS_SESSION_TOKEN: ${{aws.login.sessionToken}}
            AWS_DEFAULT_REGION: us-west-2
    """)

    esc_env = pulumiservice.Environment(
        f"esc-{env_name}",
        name=env_name,
        organization=ORG_NAME,
        project="default",
        yaml=pulumi.Output.secret(esc_yaml),
    )
    created_esc_envs.append(esc_env)

# Export Summary
pulumi.export("teamsConfigured", list(created_teams.keys()))
pulumi.export("escEnvironmentsConfigured", [e["env_name"] for e in ESC_ACCOUNTS])
