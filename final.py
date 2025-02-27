from flask import Flask, request, jsonify, abort
import os
import requests
import flask
import openai
from openai import AzureOpenAI
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)



# AzureOpenAI configuration
endpoint = os.environ.get("AOAIEndpoint")
api_key = os.environ.get("AOAIKey")
deployment = os.environ.get("AOAIDeploymentId")
tenant_id = os.environ.get("TenantId")   
client_id = os.environ.get("ClientId")  
client_secret = os.environ.get("ClientSecret") 

client = AzureOpenAI(
    base_url=f"{endpoint}/openai/deployments/{deployment}/extensions",
    api_key=api_key,
    api_version="2023-08-01-preview",
)

# Function to get Azure AD access token
def get_access_token():
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
    }
    token_response = requests.post(token_url, data=token_data)
    return token_response.json().get("access_token")

# Function to create OpenAI response
def create_openai_response(user_message):
    try:

        # Validate JSON request
        if not request.is_json:
            abort(400, "Invalid request format: Please send JSON data.")
        data = request.get_json()
        user_message = data.get("message")
        if not user_message:
            abort(400, "Missing required field: 'message'")

        access_token = get_access_token()

        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "user",
                    "content": user_message, 
                },
            ],
            extra_body={
                "dataSources": [
                    {
                        "type": "AzureCognitiveSearch",
                        "parameters": {
                            "endpoint": os.environ("SearchEndpoint"),
                            "key": os.environ("SearchKey"),
                            "indexName": os.environ("SearchIndex"),
                        }
                    }
                ]
            },
            temperature=0.7,
            top_p=1,
            max_tokens=800,

        )
        openai_response = completion.choices[0].message.content

        return openai_response
    except Exception as e:
        return jsonify({"error": f"Error: {e}"}), 500

# Route for receiving JSON POST requests
@app.route("/chat", methods=["POST"])
def receive_chat_request():
    try:
        user_message = create_openai_response(request.json)
        return jsonify({"response": user_message})
    except Exception as e:
        # Handle exceptions and return meaningful error response
        return jsonify({"error": f"Error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=False)