# AWS Application Load Balancing (Pulumi YAML)

This example provisions a high-availability Application Load Balancer (ALB) deployment.

## Architecture Highlights
- **Strict HTTPS Redirection**: Listens on port 80 and automatically responds with an HTTP 301 Permanent Redirect to port 443.
- **Modern TLS Negotiation**: Enforces the `ELBSecurityPolicy-TLS13-1-2-2021-06` security policy, restricting cipher suites to modern TLS 1.2 and TLS 1.3 standards.
- **Header Sanitization**: Enables `dropInvalidHeaderFields: true` to prevent HTTP smuggling attacks.
- **Target Group Health Checking**: Validates backend microservice availability over `/healthz` on port 8080 before routing traffic.
- **Cross-Stack Wiring**: Bridges the public networking tier with the private compute tier using StackReferences.
