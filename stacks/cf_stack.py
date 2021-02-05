#######################################################################################
#
# cf_stack.py
#
# Resources:
#  cf distribution
#  r53 Alias A Record to point your cdn subdomain to your CloudFront distribution
#
######################################################################################

from aws_cdk import (
  aws_cloudfront as cloudfront,
  aws_cloudfront_origins as origins,
  aws_route53 as rt53,
  aws_route53_targets as targets,
  core
)

import os.path

class CFStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, s3_bucket, acm_cert, hosted_zone, env, vars, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # get CDN subdomain from vars.py file
    cdn_domain=vars['cdn_domain']

    # Create the CloudFront Distribution
    cf_dist=cloudfront.Distribution(self,"CloudFront Dist",
       default_behavior=cloudfront.BehaviorOptions(
         origin=origins.S3Origin(s3_bucket),
         viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
       ),
       certificate=acm_cert,
       default_root_object="index.html",
       domain_names=[cdn_domain]
    )

    # Create the Alias Record
    rt53.ARecord(self,'CFSiteAliasRecord',
      record_name=cdn_domain,
      target=rt53.AddressRecordTarget.from_alias(targets.CloudFrontTarget(cf_dist)),
      zone=hosted_zone
    )
