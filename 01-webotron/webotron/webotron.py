#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Webotron deploys websites with aws


"""

import boto3
import sys
import click
from botocore.exceptions import ClientError
from pathlib import Path
import mimetypes
import os
#print(sys.argv)

from bucket import BucketManager

session = boto3.Session(profile_name='pythonaws')
bucketmanager = BucketManager(session)
s3 = session.resource('s3')

@click.group()
def cli():
    "webotron deplous a websites to AWS"
    pass

@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets!"
    for bucket in bucketmanager.all_buckets():
       print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List objects in S3 bucket"
    for obj in bucketmanager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "Create and configure S3 website bucket"
    s3_bucket = bucketmanager.init_bucket(bucket)
    bucketmanager.set_policy(s3_bucket)
    bucketmanager.configure_website(s3_bucket)
    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    "Sync contents of folder to Bucket"
    bucketmanager.sync(pathname, bucket)

if __name__ == '__main__':
    cli()

    