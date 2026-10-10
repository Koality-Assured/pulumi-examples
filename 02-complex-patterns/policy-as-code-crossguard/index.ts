import { PolicyPack, validateResourceOfType } from "@pulumi/policy";
import * as aws from "@pulumi/aws";
import { AwsGuard } from "@pulumi/awsguard";

// 1. Initialize AWSGuard with baseline rules
new AwsGuard({ all: "advisory" });

// 2. Custom Policy Pack definitions
new PolicyPack("enterprise-security-guardrails", {
  policies: [
    // Policy 1: Require Standard Tags on all Tagged AWS Resources
    {
      name: "require-standard-tags",
      description: "Ensures all taggable AWS resources define Environment and Service tags.",
      enforcementLevel: "mandatory",
      validateResource: (args, reportViolation) => {
        const requiredTags = ["Environment", "Service"];
        const tags = args.props.tags;
        if (!tags) {
          reportViolation(`Resource of type ${args.type} must define tags.`);
          return;
        }
        for (const tag of requiredTags) {
          if (!tags[tag] || tags[tag].trim() === "") {
            reportViolation(
              `Resource of type ${args.type} is missing required tag '${tag}'.`
            );
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

    // Policy 3: Prohibit Unencrypted S3 Buckets
    {
      name: "require-s3-encryption",
      description: "S3 buckets must not have server-side encryption disabled.",
      enforcementLevel: "mandatory",
      validateResource: validateResourceOfType(aws.s3.BucketV2, (bucket, args, reportViolation) => {
        // Validation logic for S3 server-side encryption configuration
        if (args.props.serverSideEncryptionConfiguration === null) {
          reportViolation("S3 bucket must configure server-side encryption with KMS or AES256.");
        }
      }),
    },
  ],
});
