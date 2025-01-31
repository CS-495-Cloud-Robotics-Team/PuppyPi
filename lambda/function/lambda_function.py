import json
import boto3
import base64
import openai
import tempfile
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

    #Parse response and grab the API key
    secret_string = get_secret_value_response['SecretString']
    secret_dict = json.loads(secret_string)
    return secret_dict.get("key")

def lambda_handler(event, context):

    '''
    TODO: Verify that exceptions return proper result to PuppyPi
    TODO: Handling for accepting data from the PuppyPi
    TODO: Sending and receiving information to OpenAI Whisper
    TODO: Prompt engineering for GPT
    TODO: Sending and receiving information for GPT models
    TODO: Maybe add verification stage for GPT output?
    TODO: Return information to the PuppyPi
    '''
    
    api_key = get_secret()
    if api_key is None:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to retrieve API key"})
        }

    # Check if our incoming data has a body
    if "body" not in event:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No file provided"})
        }

    try:
        # Decode the Base64-encoded MP3 file received from API Gateway
        file_content = base64.b64decode(event["body"])

        # Save file temporarily for Whisper API since it requires a file format and not binary
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
            temp_audio.write(file_content)
            temp_audio.flush()  # Ensure data is written before passing it to Whisper
            
            # Set OpenAI API key
            openai.api_key = api_key

            # Call OpenAI Whisper API
            with open(temp_audio.name, "rb") as audio_file:
                response = openai.Audio.transcribe("whisper-1", audio_file)

        # Extract transcription text
        transcription_text = response.get("text", "")

        return {
            "statusCode": 200,
            "body": json.dumps({"transcription": transcription_text})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
