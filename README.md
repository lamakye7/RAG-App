# Azure OpenAI Chatbot API
This repository contains a simple Flask-based API that integrates with Azure OpenAI to process user queries and generate responses. The API also uses Azure Active Directory for authentication and Azure Cognitive Search for retrieving relevant data.

## Features
- Accepts user messages via a `/chat` endpoint.
- Authenticates using Azure AD.
- Queries OpenAI with context from Azure Cognitive Search.
- Returns AI-generated responses.

## Tech Stack
- **Flask** (Python web framework)
- **Azure OpenAI** (AI-powered text generation)
- **Azure Active Directory** (Authentication)
- **Azure Cognitive Search** (Search and retrieval)
- **Requests** (HTTP requests handling)
- **dotenv** (Environment variable management)

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/lamakye7/RAG-App.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file:
   ```env
   AOAIEndpoint=<your_openai_endpoint>
   AOAIKey=<your_openai_api_key>
   AOAIDeploymentId=<your_openai_deployment_id>
   TenantId=<your_tenant_id>
   ClientId=<your_client_id>
   ClientSecret=<your_client_secret>
   SearchEndpoint=<your_search_endpoint>
   SearchKey=<your_search_key>
   SearchIndex=<your_search_index>
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Send a POST request to the API:
   ```json
   {
       "message": "Hello, how are you?"
   }
   ```
   Endpoint: `http://localhost:5000/chat`


