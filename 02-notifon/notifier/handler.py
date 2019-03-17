import json


def hello(event, context):
    print("Here comes the event")
    print(event)
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }

