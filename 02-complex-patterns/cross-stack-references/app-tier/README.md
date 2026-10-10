# Application Tier Micro-Stack

This stack consumes network tier exports dynamically using `pulumi:pulumi:StackReference`:
```yaml
resources:
  networkStack:
    type: pulumi:pulumi:StackReference
    properties:
      name: sample-org/pattern-cross-stack-network/prod
```
The stack retrieves `${networkStack.outputs["vpcId"]}` and `${networkStack.outputs["vpcCidr"]}` without hardcoding IDs or requiring a monolithic single-stack deployment.
