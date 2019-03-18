import os
import requests

def post_to_slack(event, context):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

    message =  '{}'.format(event['detail']['Description'])
    requests.post(slack_webhook_url, message)
    return

