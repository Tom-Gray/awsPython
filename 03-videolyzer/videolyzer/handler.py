import urllib
import boto3


def start_label_detection(bucket, key):
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.start_label_detection(
        Video={'S3Object': {'Bucket': bucket, 'Name': key}})

    print(response)


def start_processing_video(event, context):
    print(event)
    for record in evenrt['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        start_label_detection(bucket, key)
    return
