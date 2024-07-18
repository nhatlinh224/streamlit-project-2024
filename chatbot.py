import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.title('ChatBot')

# Hugging Face credentials
with st.sidebar:
    st.title("Login Hugchat")
    hf_email = st.text_input('Enter E-mail:')
    hf_pass = st.text_input('Enter Password:', type='password')
    if not (hf_email and hf_pass):
        st.warning('Please enter your account!', icon="⚠️")
    else:
        st.success('Proceed to entering your prompt message!', icon="👍")

# Store LLM generated responses
if 'messages' not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response


def generate_response(prompt_input, email, passwd):
    try:
        # Hugging Face Login
        sign = Login(email, passwd)
        cookies = sign.login()
        # Create ChatBot
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        # Send user prompt to ChatBot
        response = chatbot.chat(prompt_input)
        return response
    except Exception as e:
        st.error(f"Login failed: {e}")
        return None


# Prompt for user input and generate response
if hf_email and hf_pass:
    if prompt := st.chat_input("Say something..."):
        # Display user message in chat message container
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Display assistant response in chat message container
        response = generate_response(prompt, hf_email, hf_pass)
        if response:
            st.session_state.messages.append(
                {"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)
else:
    st.warning("Please enter your Hugging Face email and password.")
