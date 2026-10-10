import { PolicyPack, validateResourceOfType } from "@pulumi/policy";
import * as aws from "@pulumi/aws";
import { AwsGuard } from "@pulumi/awsguard";

// 1. Initialize AWSGuard with baseline rules
new AwsGuard({ all: "advisory" });

// 2. Custom Policy Pack definitions
new PolicyPack("enterprise-security-guardrails", {
  policies: [
    // Policy 1: Require Standard Tags on all Taggable AWS Resources
    {
      name: "require-standard-tags",
      description: "Ensures all taggable AWS resources define Environment and Service tags.",
      enforcementLevel: "mandatory",
      validateResource: (args, reportViolation) => {
        // Guard: Only validate resources that support a tags schema property
        if (args.props && "tags" in args.props) {
          const requiredTags = ["Environment", "Service"];
          const tags = args.props.tags;
          if (!tags || typeof tags !== "object") {
            reportViolation(`Taggable resource of type ${args.type} must define a valid tags object.`);
            return;
          }
          for (const tag of requiredTags) {
            if (!tags[tag] || typeof tags[tag] !== "string" || tags[tag].trim() === "") {
              reportViolation(
                `Resource of type ${args.type} is missing required tag '${tag}'.`
              );
            }
          }
        }
      },
    },

    // Policy 2: Enforce IMDSv2 on EC2 Instances
    {
      name: "require-ec2-imdsv2",
      description: "EC2 instances must enforce IMDSv2 with httpTokens set to 'required'.",
      enforcementLevel: "mandatory",
      validateResource: validateResourceOfType(aws.ec2.Instance, (instance, args, reportViolation) => {
        const metadataOptions = instance.metadataOptions;
        if (!metadataOptions || metadataOptions.httpTokens !== "required") {
          reportViolation(
            "EC2 instance must configure metadataOptions with httpTokens set to 'required' to prevent SSRF credential theft."
          );
        }
      }),
    },

    // Policy 3: Enforce Server-Side Encryption on S3 Configuration Resources
    {
      name: "require-s3-encryption",
      description: "S3 bucket encryption configuration must specify a valid server-side encryption algorithm.",
      enforcementLevel: "mandatory",
      validateResource: validateResourceOfType(
        aws.s3.BucketServerSideEncryptionConfigurationV2,
        (sseConfig, args, reportViolation) => {
          const rules = sseConfig.rules;
          if (!rules || rules.length === 0) {
            reportViolation("S3 bucket encryption configuration must declare at least one encryption rule.");
            return;
          }
          const defaultEncryption = rules[0].applyServerSideEncryptionByDefault;
          if (!defaultEncryption || !defaultEncryption.sseAlgorithm) {
            reportViolation(
              "S3 bucket encryption rule must define applyServerSideEncryptionByDefault with sseAlgorithm ('aws:kms' or 'AES256')."
            );
          }
        }
      ),
    },
  ],
});
