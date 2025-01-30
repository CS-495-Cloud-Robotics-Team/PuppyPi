import json
import boto3
from botocore.exceptions import ClientError

def get_secret():
    
    secret_name = "crawford_openai_api_key"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return secret

def lambda_handler(event, context):

    '''
    TODO: Grab value from key-pair
    TODO: Verify that exceptions return proper result to PuppyPi
    TODO: Handling for accepting data from the PuppyPi
    TODO: Sending and receiving information to OpenAI Whisper
    TODO: Prompt engineering for GPT
    TODO: Sending and receiving information for GPT models
    TODO: Maybe add verification stage for GPT output?
    TODO: Return information to the PuppyPi
    '''
    
    api_key = get_secret()

    # if api_key is None:
    #     return {
    #         "statusCode": 500,
    #         "body": json.dumps({"error": "Failed to retrieve API key"})
    #     }

    return {
        'statusCode': 200,
        'body': json.dumps('Hello world!')
    }
