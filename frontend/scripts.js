document.addEventListener("DOMContentLoaded", function () {
    // Global variables for active endpoints
    let activeBot = "GPT-4"; // Default active bot (GPT-4)
    let botAPI = "http://localhost:7071/api/ChatGpt_api"; // GPT-4 endpoint
    const botImage = document.querySelector(".chat-header img");
    const chatHeader = document.querySelector(".chat-header h2");

    // Set default bot image and header text for GPT-4
   // botImage.src = "assets/chatgpt.png";
    //chatHeader.innerHTML = `<img src="assets/chatgpt.png" alt="GPT-4"> GPT-4 Chat Bot`;

    // Sidebar links: When a user clicks, update the active bot, API endpoint, and header image/text.
    const botLinks = document.querySelectorAll(".sidebar ul li a");
    botLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent page reload

            activeBot = this.textContent.trim(); // Get selected bot name

            // Set corresponding bot API & image explicitly
            switch (activeBot) {
                case "GPT-4":
                    botAPI = "http://localhost:7071/api/ChatGpt_api";
                    botImage.src = "assets/chatgpt.png";
                    break;
                case "DeepSeek":
                    botAPI = "http://localhost:7071/api/DeepSeek_api";
                    botImage.src = "assets/deepseek.png";
                    break;
                
            }

            // Update header text while keeping the image (replace the entire header content)
            chatHeader.innerHTML = `<img src="${botImage.src}" alt="${activeBot}"> ${activeBot} Chat Bot`;

            // Clear the chat box when switching bots
            document.getElementById("chatBox").innerHTML = `<div class="message bot-message">🔄 Switched to ${activeBot}.</div>`;
        });
    });

    // Helper function: Formats any code blocks in the response (if needed)
    function formatMessage(message) {
        return message.replace(/```([\s\S]*?)```/g, (match, codeContent) => {
            return `<pre class="code-block"><code>${codeContent}</code></pre>`;
        });
    }

    // Helper function: Retry fetch in case of a 429 Too Many Requests error
    async function fetchWithRetry(url, options, retries = 3, delay = 2000) {
        for (let i = 0; i < retries; i++) {
            let response = await fetch(url, options);
            if (response.status !== 429) return response;
            console.warn(`⚠️ Rate limited. Retrying in ${delay / 1000}s...`);
            await new Promise(res => setTimeout(res, delay));
        }
        throw new Error("❌ Too many requests, try again later.");
    }

    // Send Message Function: Sends the same message to both GPT-4 and DeepSeek endpoints
    async function sendMessage() {
        const userInputElem = document.getElementById("userInput");
        const message = userInputElem.value.trim();
        if (!message) return;

        // Clear the input field
        userInputElem.value = "";

        // Get chat boxes for GPT-4 and DeepSeek (assumed to be side-by-side)
        const chatBoxChatGPT = document.getElementById("chatBoxChatGPT");
        const chatBoxDeepSeek = document.getElementById("chatBoxDeepSeek");

        // Append the user's message to both chat boxes
        const userMsgHTML = `<div class="message user-message">${message}</div>`;
        chatBoxChatGPT.innerHTML += userMsgHTML;
        chatBoxDeepSeek.innerHTML += userMsgHTML;

        try {
            // Send both API requests concurrently
            const [dataGPT, dataDeepSeek] = await Promise.all([
                fetchWithRetry(botAPI, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message })
                }).then(res => res.json()),
                fetchWithRetry("http://localhost:7071/api/DeepSeek_api", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message })
                }).then(res => res.json())
            ]);

            // Extract replies (fallback if missing)
            const replyGPT = dataGPT.reply || "GPT-4 did not respond.";
            const replyDeepSeek = dataDeepSeek.reply || "DeepSeek did not respond.";

            // Format the messages (if there are code blocks, etc.)
            const formattedReplyGPT = formatMessage(replyGPT);
            const formattedReplyDeepSeek = formatMessage(replyDeepSeek);

            // Append bot replies to their respective chat boxes
            chatBoxChatGPT.innerHTML += `<div class="message bot-message">${formattedReplyGPT}</div>`;
            chatBoxDeepSeek.innerHTML += `<div class="message bot-message">${formattedReplyDeepSeek}</div>`;

            // Scroll chat boxes to the bottom
            chatBoxChatGPT.scrollTop = chatBoxChatGPT.scrollHeight;
            chatBoxDeepSeek.scrollTop = chatBoxDeepSeek.scrollHeight;
        } catch (error) {
            console.error("Error:", error);
            chatBoxChatGPT.innerHTML += `<div class="message bot-message">❌ Error connecting to GPT-4 server.</div>`;
            chatBoxDeepSeek.innerHTML += `<div class="message bot-message">❌ Error connecting to DeepSeek server.</div>`;
        }
    }

    // Expose sendMessage to the global scope so that the HTML button can call it.
    window.sendMessage = sendMessage;
});
