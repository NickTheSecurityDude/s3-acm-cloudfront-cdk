#!/usr/bin/env python3

##################################################################
#
# app.py - STACKS
# 
# 1. s3
#
# Requires:
# vars.py
#
# Notes:
#  bootstrap one for project root
#  cdk bootstrap aws://<account-id>/<region>
#
###################################################################

from aws_cdk import core

import boto3
import sys

client = boto3.client('sts')

#sys.path.append("..")
import vars
#print(vars.project_vars)

region=client.meta.region_name

# CloudFront requires us-east-1
if region != 'us-east-1':
  print("This app may only be run from us-east-1")
  sys.exit()

account_id = client.get_caller_identity()["Account"]

my_env = {'region': region, 'account': account_id}

from stacks.s3_stack import S3Stack
from stacks.acm_stack import ACMStack
from stacks.cf_stack import CFStack

# Get sub project name from vars file
proj_name="s3cf
#vars.project_vars['s3_stack_name']

app = core.App()

s3_stack=S3Stack(app, proj_name+"-s3",env=my_env,vars=vars.project_vars)
acm_stack=ACMStack(app, proj_name+"-acm",env=my_env,vars=vars.project_vars)
cf_stack=CFStack(app, proj_name+"-cf",
  s3_stack.s3_bucket,
  acm_stack.acm_cert,
  acm_stack.hosted_zone,
  env=my_env,
  vars=vars.project_vars
)

# Tag all resources
for stack in [s3_stack,acm_stack,cf_stack]:
  core.Tags.of(stack).add("Project", proj_name)
  core.Tags.of(stack).add("ProjectGroup", vars.project_vars['group_proj_name'])

app.synth()
