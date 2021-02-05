##############################################################
#
# acm_stack.py
#
# Resources:
#  acm certificate
#
##############################################################

from aws_cdk import (
  aws_certificatemanager as acm,
  aws_route53 as rt53,
  core
)

import os.path,boto3

class ACMStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, env, vars, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    rt53_client = boto3.client('route53')

    # get domain name from vars.py file
    domain_name=vars['domain_name']

    # get hosted zone ID
    # change to use pagination if over 100 zones
    response = rt53_client.list_hosted_zones()
    h_zones=response['HostedZones']
    for h_zone in h_zones:
      name=h_zone['Name']
      if name[0:-1] == domain_name:
        h_zone_id=h_zone['Id'].split("/")[2]
        #print(h_zone_id)

    # create an IHostedZone object
    self._hosted_zone=rt53.HostedZone.from_hosted_zone_attributes(self,"fhzi",
      hosted_zone_id=h_zone_id,
      zone_name=domain_name)

    # Create the ACM certificate, this will do DNS validation automagically
    self._acm_cert=acm.Certificate(self,"CF SSL Cert",
      domain_name=vars['cdn_domain'],
      validation=acm.CertificateValidation.from_dns(self._hosted_zone)
    )

  # Exports
  @property
  def acm_cert(self) -> acm.ICertificate:
    return self._acm_cert

  @property
  def hosted_zone(self) -> rt53.IHostedZone:
    return self._hosted_zone
  