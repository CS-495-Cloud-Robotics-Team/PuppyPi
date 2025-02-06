import json
import boto3
import base64
import openai
import tempfile
from botocore.exceptions import ClientError

def get_commands():
    return ["2_legs_stand", 
            "bow", 
            "boxing",
            "grab",
            "jump",
            "kick_ball_left",
            "kick_ball_right",
            "lie_down",
            "look_down",
            "moonwalk",
            "nod",
            "pee",
            "push-up",
            "shake_hands",
            "sit",
            "spacewalk",
            "stand_with_arm",
            "stand",
            "stretch",
            "wave"]

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
        raise e

    #Parse response and grab the API key
    secret_string = get_secret_value_response['SecretString']
    secret_dict = json.loads(secret_string)
    return secret_dict.get("key")

def lambda_handler(event, context):

    '''
    TODO: Verify that exceptions return proper result to PuppyPi
    TODO: Prompt engineering for GPT
    TODO: Maybe add verification stage for GPT output?
    TODO: Return information to the PuppyPi
    '''
    
    api_key = get_secret()
    if api_key is None: # check if our api key retrieval failed
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to retrieve API key"})
        }

    # Check if our incoming data has a body
    # Could be improved
    if "body" not in event:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No file provided"})
        }

    try:
        # Decode the Base64-encoded MP3 file received from API Gateway, may need to be verified
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

        # Send transcription to GPT-3.5-turbo for further processing
        gpt_response = interpret_audio(transcription_text)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "transcription": transcription_text,
                "gpt_analysis": gpt_response
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    return {
                "statusCode": 400,
                "body": json.dumps({"Error": "Reached end of API"})
            }

def interpret_audio(transcription_text):
    
    """Send a prompt to OpenAI's GPT-3.5-TURBO and return the response."""
    system_prompt = f"""
    You are an AI that classifies spoken commands into predefined commands for a robotic quadruped.
    The valid commands are: {", ".join(get_commands())}.

    Your task is to analyze the given user input and return the **single best matching command** from the predefined list.

    - Only return one of the commands: {", ".join(get_commands())}.
    - Do not add any extra words, explanations, or formatting.

    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcription_text}
        ]
    )

    return response["choices"][0]["message"]["content"]