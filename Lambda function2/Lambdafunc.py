import boto3
client = boto3.client('lambda')
response = client.invoke(
    FunctionName='slack_botv3',
    InvocationType='Event'
)
print(response['StatusCode'])