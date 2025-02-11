css = '''
<style>
:root {
    /* Color Palette */
    --primary-color: #4a90e2;
    --secondary-color: #2ecc71;
    --background-color: #f7f9fc;
    --text-primary: #2c3e50;
    --text-secondary: #7f8c8d;
    --chat-bg-light: #ffffff;
    --chat-bg-dark: #f0f4f8;
    
    /* Gradient Backgrounds */
    --gradient-primary: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    --gradient-secondary: linear-gradient(135deg, #2ecc71 0%, #3498db 100%);
}

header {
display : none !important;

}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    scrollbar-width: thin;
    scrollbar-color: var(--primary-color) transparent;
}


body {
    font-family: 'Nunito', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background-color: var(--background-color);
    line-height: 1.6;
    color: var(--text-primary);
}


.stApp {
    max-width: 80%;
    max-hight: 60%;
    margin: 20px auto;
    background-color: var(--chat-bg-light);
    box-shadow: 0 15px 35px rgba(0,0,0,0.08);
    border-radius: 20px;
    overflow: hidden;
    transition: all 0.3s ease;
}



/* Buttons */
.stButton > button {
    background: var(--gradient-secondary);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    font-weight: 600;
    transition: transform 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.main-container {
    display: flex;
    width: 100%;
    height: 100vh;
    overflow: hidden;
}

.sidebar-container {
    width: 300px;
    background-color: var(--chat-bg-light);
    border-right: 1px solid var(--chat-bg-dark);
    padding: 20px;
    overflow-y: auto;
}

.chat-container {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    height: 100vh;
    background: var(--chat-bg-dark);
    padding: 20px;
}

.chat-messages {
    flex-grow: 1;
    overflow-y: auto;
    padding: 15px;
    background: var(--chat-bg-light);
    border-radius: 15px;
    margin-bottom: 15px;
}

.chat-input-area {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: var(--chat-bg-light);
    border-radius: 15px;
}

.chat-message {
    display: flex;
    align-items: flex-end;
    margin-bottom: 20px;
    max-width: 90%;
}

.chat-message.user {
    margin-left: auto;
    flex-direction: row-reverse;
}

.chat-message.bot {
    margin-right: auto;
}

.chat-message.user .message {
    background: var(--gradient-primary);
    color: white;
    border-radius: 15px 15px 0 15px;
}

.chat-message.bot .message {
    background: var(--chat-bg-dark);
    color: var(--text-primary);
    border-radius: 15px 15px 15px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.chat-message .avatar {
    width: 50px;
    height: 50px;
    margin: 0 10px;
    flex-shrink: 0;
}

.chat-message .avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid var(--primary-color);
}

.chat-message .message {
    padding: 12px 18px;
    max-width: calc(100% - 80px);
    line-height: 1.5;
    font-size: 15px;
    word-wrap: break-word;
}

/* Scrollbar */
.chat-messages::-webkit-scrollbar {
    width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
    background: var(--chat-bg-light);
}

.chat-messages::-webkit-scrollbar-thumb {
    background: var(--primary-color);
    border-radius: 10px;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/Qjjsf2p/synapse.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://media.licdn.com/dms/image/v2/D4E03AQHmcRQDv_bk0A/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1715424490719?e=2147483647&v=beta&t=OqpHUboa4AmvNtm-q0_tGyCpmWBrRTwyQMfErGAjavk">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
