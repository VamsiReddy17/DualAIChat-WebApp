document.addEventListener("DOMContentLoaded", function () {
    // Global variables
    const userInputElem = document.getElementById("userInput");
    const sendButton = document.getElementById("sendButton");
    const charCount = document.getElementById("charCount");

    // Initialize character counter
    updateCharacterCount();

    // Auto-resize textarea
    userInputElem.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        updateCharacterCount();
        updateSendButton();
    });

    // Enter key handling
    userInputElem.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Update character count
    function updateCharacterCount() {
        const count = userInputElem.value.length;
        charCount.textContent = count;
        charCount.style.color = count > 1800 ? 'var(--error-color)' : 'var(--text-muted)';
    }

    // Update send button state
    function updateSendButton() {
        const hasText = userInputElem.value.trim().length > 0;
        sendButton.disabled = !hasText;
    }

    // Clear chat function
    window.clearChat = function(chatBoxId) {
        const chatBox = document.getElementById(chatBoxId);
        const botName = chatBoxId.includes('ChatGPT') ? 'GPT-4' : 'DeepSeek';
        const icon = chatBoxId.includes('ChatGPT') ? '🤖' : '🧠';
        const message = chatBoxId.includes('ChatGPT') ? 
            "I'm ready to help you with any questions or tasks!" :
            "Let's explore ideas and solve problems together!";

        chatBox.innerHTML = `
            <div class="welcome-message">
                <div class="welcome-icon">${icon}</div>
                <h4>Welcome to ${botName}</h4>
                <p>${message}</p>
            </div>
        `;
    };

    // Show typing indicator
    function showTypingIndicator(botType) {
        const indicator = document.getElementById(`typing${botType}`);
        if (indicator) {
            indicator.style.display = 'flex';
        }
    }

    // Hide typing indicator
    function hideTypingIndicator(botType) {
        const indicator = document.getElementById(`typing${botType}`);
        if (indicator) {
            indicator.style.display = 'none';
        }
    }

    // Format message with code blocks and better styling
    function formatMessage(message) {
        // Handle code blocks
        message = message.replace(/```([\s\S]*?)```/g, (match, codeContent) => {
            return `<pre class="code-block"><code>${codeContent.trim()}</code></pre>`;
        });

        // Handle inline code
        message = message.replace(/`([^`]+)`/g, '<code style="background: #e2e8f0; padding: 0.125rem 0.25rem; border-radius: 0.25rem; font-size: 0.875em;">$1</code>');

        // Handle line breaks
        message = message.replace(/\n/g, '<br>');

        return message;
    }

    // Retry mechanism with exponential backoff
    async function fetchWithRetry(url, options, retries = 3, delay = 1000) {
        for (let i = 0; i < retries; i++) {
            try {
                const response = await fetch(url, options);
                if (response.status !== 429) return response;
                console.warn(`⚠️ Rate limited. Retrying in ${delay / 1000}s...`);
                await new Promise(res => setTimeout(res, delay));
                delay *= 2; // Exponential backoff
            } catch (error) {
                if (i === retries - 1) throw error;
                console.warn(`⚠️ Request failed. Retrying in ${delay / 1000}s...`);
                await new Promise(res => setTimeout(res, delay));
                delay *= 2;
            }
        }
        throw new Error("❌ Too many requests, try again later.");
    }

    // Add timestamp to messages
    function getCurrentTime() {
        return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    // Send message function
    async function sendMessage() {
        const message = userInputElem.value.trim();
        if (!message || sendButton.disabled) return;

        // Clear input and update UI
        userInputElem.value = "";
        userInputElem.style.height = 'auto';
        updateCharacterCount();
        updateSendButton();
        sendButton.disabled = true;

        // Get chat boxes
        const chatBoxChatGPT = document.getElementById("chatBoxChatGPT");
        const chatBoxDeepSeek = document.getElementById("chatBoxDeepSeek");

        // Clear welcome messages if they exist
        const welcomeGPT = chatBoxChatGPT.querySelector('.welcome-message');
        const welcomeDeepSeek = chatBoxDeepSeek.querySelector('.welcome-message');
        if (welcomeGPT) welcomeGPT.remove();
        if (welcomeDeepSeek) welcomeDeepSeek.remove();

        // Add user message with timestamp
        const timestamp = getCurrentTime();
        const userMsgHTML = `
            <div class="message user-message">
                ${formatMessage(message)}
                <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;">${timestamp}</div>
            </div>
        `;
        chatBoxChatGPT.innerHTML += userMsgHTML;
        chatBoxDeepSeek.innerHTML += userMsgHTML;

        // Scroll to bottom
        chatBoxChatGPT.scrollTop = chatBoxChatGPT.scrollHeight;
        chatBoxDeepSeek.scrollTop = chatBoxDeepSeek.scrollHeight;

        // Show typing indicators
        showTypingIndicator('GPT');
        showTypingIndicator('DeepSeek');

        // API Configuration - Use backend server on port 7071
        const currentUrl = window.location.href;
        let apiBaseUrl;
        
        if (currentUrl.includes('replit.dev')) {
            // For Replit, construct the backend URL using the 3000 external port mapping
            const hostname = window.location.hostname;
            
            if (hostname.includes('--80-')) {
                // Replace --80- with --3000- (backend external port)
                const backendHostname = hostname.replace('--80-', '--3000-');
                apiBaseUrl = `https://${backendHostname}`;
            } else {
                // Extract the repl ID and construct backend URL
                const replId = hostname.split('.')[0];
                apiBaseUrl = `https://${replId}--3000.replit.dev`;
            }
        } else {
            // Fallback for local development
            apiBaseUrl = 'http://localhost:7071';
        }
        
        console.log('🔗 Using API base URL:', apiBaseUrl);

        try {
            // Send requests to both APIs
            const [responseGPT, responseDeepSeek] = await Promise.allSettled([
                fetchWithRetry(`${apiBaseUrl}/api/ChatGpt_api`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message })
                }),
                fetchWithRetry(`${apiBaseUrl}/api/DeepSeek_api`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message })
                })
            ]);

            // Handle GPT-4 response
            hideTypingIndicator('GPT');
            if (responseGPT.status === 'fulfilled') {
                try {
                    const dataGPT = await responseGPT.value.json();
                    const replyGPT = dataGPT.reply || "GPT-4 did not respond.";
                    const formattedReplyGPT = formatMessage(replyGPT);
                    const responseTime = getCurrentTime();

                    chatBoxChatGPT.innerHTML += `
                        <div class="message bot-message">
                            ${formattedReplyGPT}
                            <div style="font-size: 0.75rem; opacity: 0.6; margin-top: 0.5rem;">${responseTime}</div>
                        </div>
                    `;
                } catch (error) {
                    console.error("Error parsing GPT-4 response:", error);
                    chatBoxChatGPT.innerHTML += `
                        <div class="message bot-message" style="color: var(--error-color);">
                            ❌ Error parsing GPT-4 response.
                        </div>
                    `;
                }
            } else {
                console.error("GPT-4 request failed:", responseGPT.reason);
                // Demo response when backend is not available
                chatBoxChatGPT.innerHTML += `
                    <div class="message bot-message" style="color: var(--warning-color);">
                        🔧 Demo Mode: GPT-4 backend not connected.<br>
                        <em>Your message: "${message}"</em><br><br>
                        This is a demo response. To get real AI responses, you need to:<br>
                        1. Set up Azure OpenAI service<br>
                        2. Configure the backend Azure Functions<br>
                        3. Add your API keys to environment variables
                    </div>
                `;
            }

            // Handle DeepSeek response
            hideTypingIndicator('DeepSeek');
            if (responseDeepSeek.status === 'fulfilled') {
                try {
                    const dataDeepSeek = await responseDeepSeek.value.json();
                    const replyDeepSeek = dataDeepSeek.reply || "DeepSeek did not respond.";
                    const formattedReplyDeepSeek = formatMessage(replyDeepSeek);
                    const responseTime = getCurrentTime();

                    chatBoxDeepSeek.innerHTML += `
                        <div class="message bot-message">
                            ${formattedReplyDeepSeek}
                            <div style="font-size: 0.75rem; opacity: 0.6; margin-top: 0.5rem;">${responseTime}</div>
                        </div>
                    `;
                } catch (error) {
                    console.error("Error parsing DeepSeek response:", error);
                    chatBoxDeepSeek.innerHTML += `
                        <div class="message bot-message" style="color: var(--error-color);">
                            ❌ Error parsing DeepSeek response.
                        </div>
                    `;
                }
            } else {
                console.error("DeepSeek request failed:", responseDeepSeek.reason);
                // Demo response when backend is not available
                chatBoxDeepSeek.innerHTML += `
                    <div class="message bot-message" style="color: var(--warning-color);">
                        🔧 Demo Mode: DeepSeek backend not connected.<br>
                        <em>Your message: "${message}"</em><br><br>
                        This is a demo response. To get real AI responses, you need to:<br>
                        1. Set up DeepSeek API access<br>
                        2. Configure the backend Azure Functions<br>
                        3. Add your API keys to environment variables
                    </div>
                `;
            }

        } catch (error) {
            console.error("Error:", error);
            hideTypingIndicator('GPT');
            hideTypingIndicator('DeepSeek');

            const errorMsg = `
                <div class="message bot-message" style="color: var(--error-color);">
                    ❌ Network error. Please check your connection and try again.
                </div>
            `;
            chatBoxChatGPT.innerHTML += errorMsg;
            chatBoxDeepSeek.innerHTML += errorMsg;
        } finally {
            // Re-enable send button
            sendButton.disabled = false;

            // Scroll to bottom
            chatBoxChatGPT.scrollTop = chatBoxChatGPT.scrollHeight;
            chatBoxDeepSeek.scrollTop = chatBoxDeepSeek.scrollHeight;

            // Focus back to input
            userInputElem.focus();
        }
    }

    // Expose functions to global scope
    window.sendMessage = sendMessage;

    // Focus input on load
    userInputElem.focus();
});