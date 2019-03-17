# coding: utf-8
import boto3
session = boto3.Session()
as_client = session.client('autoscaling')

as_client.execute_policy(AutoScalingGroupName='Notifon Example ASG', PolicyName='Scale Up')