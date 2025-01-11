import streamlit as st
import requests

# Replace with your Ollama endpoint URL
OLLAMA_API_URL = "http://localhost:11434/api/chat"

# Replace with your model name (e.g., "llama")
MODEL_NAME = "llama"

# Streamlit Layout
st.title("💬 Chat with LLama")
st.markdown("A simple chat interface powered by LLama running on Ollama.")

# Initialize empty list for conversation context
conversation_context = []

# User input box
user_input = st.text_input("Type your message here:")

if st.button("Send"):
    if user_input.strip():
        # Add user message to the context
        conversation_context.append({"role": "user", "content": user_input})

        try:
            # Send request to the Ollama API
            response = requests.post(
                OLLAMA_API_URL,
                json={"model": MODEL_NAME, "messages": conversation_context},
                headers={"Content-Type": "application/json"},
            )
            response_data = response.json()

            if response.status_code == 200:
                # Get assistant's response and add to the context
                assistant_reply = response_data.get("content", "")
                conversation_context.append({"role": "assistant", "content": assistant_reply})

                # Display the conversation
                st.markdown(f"**You:** {user_input}")
                st.markdown(f"**LLama:** {assistant_reply}")
            else:
                st.error(f"Error: {response_data.get('error', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please enter a message before sending.")
