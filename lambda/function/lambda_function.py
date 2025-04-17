import json
import boto3
import base64
import openai
import tempfile
from botocore.exceptions import ClientError

def get_commands():
    return [
        "two-legs-stand",
        "bow",
        "boxing-main",
        "boxing-alt",
        "grab",
        "jump",
        "kick-ball-left",
        "kick-ball-left-bak",
        "kick-ball-right",
        "lie-down",
        "look-down-short",
        "look-down",
        "moonwalk",
        "nod",
        "pee",
        # "place-main",
        # "place-alt",
        "push-up",
        "run",
        "shake-hands",
        "shake-head",
        "sit",
        "spacewalk",
        "stand-short",
        "stand",
        # "stand-with-arm",
        "stretch",
        "turn-around",
        "turn-left",
        "turn-right",
        # "up-stairs-2cm",
        # "up-stairs-3.5cm",
        # "up-stairs-3.5cm-alt0",
        # "up-stairs-3.5cm-alt1",
        "walk",
        "walk-backward",
        "wave",
        "face-detect",
        "black-line-following",
        "red-line-following",
        "color-detect",
        "apriltag-detect",
        "lidar-avoidance",
        "lidar-tracking",
        "lidar-guarding"
    ]

def get_secret():
    
    secret_name = "crawford_openai_api_key"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret_string = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret_string)
        return secret_dict.get("key")
    except ClientError as e:
        print(f"Error retrieving secret: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding secret JSON: {e}")
        return None 
    except Exception as e:
        print(f"Non-trivial error: {e}")
        return None

def lambda_handler(event, context):

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
        file_content = base64.b64decode(event["body"])
    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"error": f"Invalid base64 encoding: {e}"})}

        # Save file temporarily for Whisper API since it requires a file format and not binary
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as temp_audio:
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
    except openai.error.OpenAIError as e:
        return {"statusCode": 500, "body": json.dumps({"error": f"OpenAI API error: {str(e)}"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": f"Unexpected error: {str(e)}"})}

    return {
                "statusCode": 400,
                "body": json.dumps({"Error": "Reached end of lambda_handler"})
            }

def interpret_audio(transcription_text):
    
    #Send a prompt to OpenAI's GPT-4.1-Nano and return the response.
    system_prompt = f"""
    You are an AI that translates spoken commands into a chronological sequence of predefined commands for a robotic quadruped.
    The valid commands are: {", ".join(get_commands())}.

    Your task is to analyze the given user input and return the **sequence of matching commands** in order.
    - Return a **JSON list** of commands in the exact order they should be executed.
    - Only include commands from this list: {", ".join(get_commands())}.
    - If a command cannot be determined, exclude it.
    - If the user input is completely unrelated, return `["error"]`.
    - An exception is if the user input is walk then a number, return `["walk", x]` where x is the number they said
    - Under no circumstances should you deviate from the response format.

    Example Inputs & Outputs:
    
    - Input: "Sit and then stand up"
      Output: `["sit", "stand"]`
      
    - Input: "Bow, shake hands, and wave"
      Output: `["bow", "shake-hands", "wave"]`
      
    - Input: "Walk for 5 seconds, then do the moonwalk"
      Output: `["walk", 5, "moonwalk"]

    - Input: "Do a backflip" (not a valid command)
      Output: `["error"]`

    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcription_text}
            ]
        )

        if "choices" not in response or not response["choices"]:
            raise ValueError("Invalid OpenAI response format")

        # Extract and return the list of commands
        command_list = json.loads(response["choices"][0]["message"]["content"])
        if not isinstance(command_list, list):
            raise ValueError("Unexpected response format: not a list")
        return command_list
    except json.JSONDecodeError:
        return ["error"]
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return ["error"]
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ["error"]
