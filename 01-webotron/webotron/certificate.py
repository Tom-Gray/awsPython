

"""Classes for ACM Certificates"""

class CertificateManager:

    def __init__(self, session):
        self.session = session
        self.client = self.session.client('acm', region_name='us-east-1')

    def find_matching_cert(self, domain_name):
        paginator = self.client.get_paginator('list_certificates')
        for page in paginator.paginate(CertificateStatuses=['ISSUED']):
            for cert in page['CertificateSummaryList']:
                if self.cert_matches(cert['DomainName'], domain_name):
                    return cert
        return None

    def cert_matches(self, cert_arn, domain_name):
        """Return True if cert matches domain_name."""
        cert_details = self.client.describe_certificate(
                CertificateArn=cert_arn
        )
        alt_names = cert_details['Certificate']['SubjectAlternativeNames']
        for name in alt_names:
            if name == domain_name:
                return True
            if name[0] == '*' and domain_name.endswith(name[1:]):
                return True
        return False

def create_cf_domain_record(self, zone, domain_name, cf_domain):
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
                                'HostedZoneId': 'Z2FDTNDATAQYW2',
                                'DNSName': cf_domain,
                                'EvaluateTargetHealth': False
                            }
                        }
                    }
                ]
            }
        )