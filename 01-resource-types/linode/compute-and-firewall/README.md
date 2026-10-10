# Linode Compute & Firewall (Pulumi YAML)

This example demonstrates deploying independent cloud compute nodes on Linode (Akamai Cloud Computing) managed via Pulumi YAML.

## Highlights
- **Cloud Firewall Inbound Filtering**: Enforces a default `DROP` policy on inbound traffic, permitting only web traffic (ports 80 and 443) and restricting administrative SSH (port 22) to designated trusted IP ranges.
- **Private Networking**: Enables `privateIp: true` on compute nodes to facilitate inter-node communication over Linode's private datacenter network without hair-pinning across public interfaces.
- **Scoped Service Tokens**: Employs fine-grained Linode API tokens (`linode:Token`) with restricted `read_only` scopes for automated monitoring and inventory collection.
