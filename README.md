**Dual AI Chatbots - Azure Web App**
Dual AI Chatbots - Azure Web App is a web application that integrates two chatbot models—GPT-4 and DeepSeek—into a single interface. A common user prompt is sent concurrently to both chatbots, and their responses are displayed side by side. This project demonstrates how to use Azure Static Web Apps for the frontend and Azure Functions for the backend to create a multi-AI integration solution.

Features
Dual AI Chatbots Interface:

GPT-4 Chat Bot: Powered by Azure OpenAI using GPT-4 (via the ChatGgpt_api Azure Function).
DeepSeek Chat Bot: Powered by DeepSeek (via the DeepSeek_api Azure Function).
Common Input:
A single input box that sends the same message to both chatbots simultaneously.

Responsive Design:
The UI is designed with HTML, CSS, and JavaScript to display the two chat windows side by side with vertical scrollbars when needed.

Retry Mechanism:
Implements a retry mechanism to handle rate-limiting (HTTP 429 errors) gracefully.

Code Formatting:
Supports formatting of code blocks within responses (wrapped in triple backticks) for clear display.
