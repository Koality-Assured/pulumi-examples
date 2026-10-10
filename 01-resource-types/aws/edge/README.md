# AWS Edge: CloudFront & WAFv2 (Pulumi YAML)

This example provisions a resilient global edge distribution using Amazon CloudFront backed by AWS WAFv2 inspection and active-passive origin failover.

## Architectural Highlights
- **Origin Failover Groups**: Defines an `originGroups` configuration binding a primary origin and a secondary failover origin. If the primary origin returns HTTP `500`, `502`, `503`, or `504`, CloudFront automatically transparently retries the request against the secondary origin without failing the viewer request.
- **Defense-in-Depth Edge WAF**: Associates an AWS WAFv2 WebACL at edge inspection points before traffic hits backend infrastructure:
  - `AWSManagedRulesCommonRuleSet` (OWASP Top 10 mitigations).
  - `AWSManagedRulesKnownBadInputsRuleSet` (Exploit string and bad payload mitigation).
  - IP-based rate limiting (2,000 requests per 5 minutes per IP address) to suppress Layer 7 volumetric floods.
- **SPA Error Routing**: Remaps HTTP 404 responses to HTTP 200 `/index.html` for single-page applications.
