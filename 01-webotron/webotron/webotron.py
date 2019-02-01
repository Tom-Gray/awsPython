import boto3
import sys
import click

print(sys.argv)
session = boto3.Session(profile_name='pythonaws')
s3 = session.resource('s3')

@click.group()
def cli():
    "webotron deplous a websites to AWS"
    pass

@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List objects in S3 bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)


if __name__ == '__main__':
    cli()

    