##############################################################
#
# s3_stack.py
#
# Resources:
#  1 - s3 bucket
#  1 - s3 deployment - not working
#
##############################################################

from aws_cdk import (
  aws_s3 as s3,
  aws_s3_deployment as deployment_,
  core
)

import os.path,time

class S3Stack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, env, vars, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)
 
    rand_num=str(time.time())[:4]
    rand_num=str(1612)

    # create the s3 bucket
    self.bucket=s3.Bucket(self,"S3-Bucket",
      bucket_name=vars['s3_stack_name']+"-bucket-"+rand_num
    )

    # NOT WORKING - CDK/NPM bug? https://github.com/aws/aws-cdk/issues/12536
    # Upload files manually
    """
    dirname = os.path.dirname(__file__)

    deployment_.BucketDeployment(self,"Web Files",
      destination_bucket=bucket,
      sources=[deployment_.Source.asset(os.path.join(dirname, "files/web_files.zip"))]
    )
    """

  # Exports
  @property
  def s3_bucket(self) -> s3.IBucket:
    return self.bucket