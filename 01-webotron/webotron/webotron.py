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

session = None
bucketmanager = None 

@click.group()
@click.option('--profile', default=None, help="Use a given AWS profile")
def cli(profile):
    "webotron deplous a websites to AWS"
    global session, bucketmanager
    session_config= {} #new dictionary
    if profile:
        session_config['profile_name'] = profile

    session = boto3.Session(**session_config) # this is like doing a @splat in powershell
    bucketmanager = BucketManager(session)

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
    print(bucketmanager.get_bucket_url(bucketmanager.s3.Bucket(bucket)))

if __name__ == '__main__':
    cli()

    