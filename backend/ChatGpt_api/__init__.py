import logging
import azure.functions as func
import json
import os
import requests

AZURE_OPENAI_KEY = os.getenv("AZURE_KEY")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing ChatGPT request.")

    if req.method == "OPTIONS":
        return func.HttpResponse(
            "",
            status_code=204,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )

    try:
        req_body = req.get_json()
        user_message = req_body.get("message", "")

        if not user_message:
            return func.HttpResponse(
                json.dumps({"error": "Message is required"}),
                status_code=400,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )

        # ✅ Using your Azure OpenAI endpoint
        url = "https://txd61-m9nyyhgs-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview"
        
        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_KEY
        }
        
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Keep responses short and direct."},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 900,
            "temperature": 0.5
        }

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        ai_response = response.json()

        if "choices" in ai_response and len(ai_response["choices"]) > 0:
            reply_text = ai_response["choices"][0]["message"]["content"]
        else:
            reply_text = "AI did not return a response."

        return func.HttpResponse(
            json.dumps({"reply": reply_text}),
            status_code=200,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Azure AI request failed", "details": str(e)}),
            status_code=500,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )
