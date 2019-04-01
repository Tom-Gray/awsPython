import boto3
from pathlib import Path


session = boto3.Session()

rekognition_client = boto3.client('rekognition')
s3 = boto3.resource('s3')
bucket = s3.create_bucket(Bucket='tomvideobucket123', CreateBucketConfiguration={'LocationConstraint': session.region_name})
bucket



path = '~/Downloads/car-driving.mp4'
path = Path(path).expanduser().resolve()
print(str(path))
print(str(path.name))

bucket.upload_file(str(path), str(path.name))

rekognition_client = boto3.client('rekognition')

response = rekognition_client.start_label_detection(Video={'S3Object': { 'Bucket': bucket.name, 'Name': path.name}})

jobId = response['JobId']

result = rekognition_client.get_label_detection(JobId=jobId)