def hello(event, context):
    for item in event['Items']:
        print(item)