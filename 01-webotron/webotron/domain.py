

import uuid

class DomainManager:
    """Manage a r53 domain"""


    def __init__(self,session):
        self.session = session
        self.client = self.session.client('route53')


    def find_hosted_zone(self, domain_name):
        paginator = self.client.get_paginator('list_hosted_zones')
        for page  in paginator.paginate():
            for zone in page['HostedZones']:
                if domain_name.endswith(zone['Name'][:-1]):
                    return zone

        return None
    
    def create_hosted_zone(self, domain_name):
        """create a zone"""
        #web.tomgray.me needs to be tomgray.me.
        zone_name = '.'.join(domain_name.split('.')[-2:]) + '.'
        return self.client.create_hosted_zone(
            Name=zone_name,
            CallerReference=str(uuid.uuid4())
            )

    def create_s3_domain_record(self, zone, domain_name, endpoint):
        """Create a domain record in zone for domain_name."""
        return self.client.change_resource_record_sets(
            HostedZoneId=zone['Id'],
            ChangeBatch={
                'Comment': 'Created by webotron',
                'Changes': [{
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': domain_name,
                            'Type': 'A',
                            'AliasTarget': {
                                'HostedZoneId': endpoint.zone,
                                'DNSName': endpoint.host,
                                'EvaluateTargetHealth': False
                            }
                        }
                    }
                ]
            }
        )

