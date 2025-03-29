# RecallrAI Python SDK

Official Python SDK for RecallrAI – a revolutionary contextual memory system that enables AI assistants to form meaningful connections between conversations, just like human memory.

## Installation

Install the SDK via Poetry or pip:

```bash
poetry add recallrai
# or
pip install recallrai
```

## Initialization

Create a client instance with your API key and project ID:

```python
from recallrai import RecallrAI

api_key = "rai_yourapikey"
project_id = "project-uuid"
client = RecallrAI(api_key=api_key, project_id=project_id)
```

## User Management

### Create a User

```python
from recallrai.user import User

user_id = "user123"
metadata = {"key": "value"}
user = client.create_user(user_id=user_id, metadata=metadata)
print("Created user:", user.user_id)
```

### Get a User

```python
user = client.get_user("user123")
print("User metadata:", user.metadata)
```

### List Users

```python
user_list = client.list_users(offset=0, limit=10)
for user in user_list.users:
    print(user.user_id, user.metadata)
```

### Update a User

```python
# Update the user's metadata and/or change the user ID
updated_user = client.update_user(user_id="user123", new_metadata={"role": "user"}, new_user_id="user1234")
print("Updated user id:", updated_user.user_id)
```

### Delete a User

```python
client.delete_user("user1234")
print("User deleted.")
```

## Session Management

### Create a Session

```python
from recallrai.session import Session

# Create a session for a user; auto_process_after_minutes set to -1 disables auto-processing.
session = client.create_session(user_id="user123", auto_process_after_minutes=5)
print("Created session id:", session.session_id)
```

### Get an Existing Session

```python
# Retrieve an existing session by its ID
session = client.get_session(user_id="user123", session_id="session-uuid")
print("Session status:", session.get_status())
```

### List Sessions

```python
session_list = client.list_sessions(user_id="user123", offset=0, limit=10)
for session in session_list.sessions:
    print(session.session_id, session.status)
```

### Session – Adding Messages

#### Add a User Message

```python
session.add_user_message("Hello! How are you?")
```

### Session – Retrieving Context

```python
context = session.get_context()
print("Memory used:", context.memory_used)
print("Context:", context.context)
```

#### Add an Assistant Message

```python
session.add_assistant_message("I'm an assistant. How can I help you?")
```

### Session – Process Session

```python
session.process()
```

### Session – Get Status and Messages

```python
status = session.get_status()
print("Session status:", status)

messages = session.get_messages()
for message in messages:
    print(f"{message.role}: {message.content} at {message.timestamp}")
```

## Example Usage with LLMs

```python
import openai
from recallrai import RecallrAI

# Initialize RecallrAI and OpenAI clients
recallrai_client = RecallrAI(api_key="rai_yourapikey", project_id="project-uuid")
openai_client = openai.OpenAI(api_key="your-openai-api-key")

def chat_with_memory(user_id, session_id=None):
    # Get or create user
    try:
        user = recallrai_client.get_user(user_id)
    except:
        user = recallrai_client.create_user(user_id)
    
    # Create a new session or get an existing one
    if session_id:
        session = recallrai_client.get_session(user_id=user_id, session_id=session_id)
    else:
        session = recallrai_client.create_session(user_id=user_id, auto_process_after_minutes=30)
        print(f"Created new session: {session.session_id}")
    
    print("Chat session started. Type 'exit' to end the conversation.")
    
    while True:
        # Get user input
        user_message = input("You: ")
        if user_message.lower() == 'exit':
            break
        
        # Add the user message to RecallrAI
        session.add_user_message(user_message)
        
        # Get context from RecallrAI after adding the user message
        context = session.get_context()
        
        # Create a system prompt that includes the context
        system_prompt = f"""You are a helpful assistant with memory of previous conversations.
        
        MEMORIES ABOUT THE USER:
        {context.context}
        
        You can use the above memories to provide better responses to the user.
        Don't mention that you have access to memories unless you are explicitly asked."""
        
        # Get previous messages
        previous_messages = session.get_messages()
        previous_messages = [{"role": message.role, "content": message.content} for message in previous_messages]

        # Call the LLM with the system prompt and user message
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                **previous_messages,
            ],
            temperature=0.7
        )
        
        assistant_message = response.choices[0].message.content
        
        # Print the assistant's response
        print(f"Assistant: {assistant_message}")
        
        # Add the assistant's response to RecallrAI
        session.add_assistant_message(assistant_message)
    
    # Process the session at the end of the conversation
    print("Processing session to update memory...")
    session.process()
    print(f"Session ended. Session ID: {session.session_id}")
    return session.session_id

# Example usage
if __name__ == "__main__":
    user_id = "user123"
    # To continue a previous session, uncomment below and provide the session ID
    # previous_session_id = "previously-saved-session-uuid"
    # session_id = chat_with_memory(user_id, previous_session_id)
    
    # Start a new session
    session_id = chat_with_memory(user_id)
    print(f"To continue this conversation later, use session ID: {session_id}")
```

## Exception Handling

> Exception handling will be improved in future.
Each operation may raise custom exceptions defined in the SDK:

```python
from recallrai.utils.exceptions import NotFoundError, ValidationError

try:
    user = client.get_user("nonexistent_id")
except NotFoundError as e:
    print("User not found:", e.message)
except ValidationError as e:
    print("Invalid input:", e.message)
```

## Conclusion

This README outlines the basic usage of the RecallrAI SDK functions for user and session management. For additional documentation and advanced usage, please see the [official documentation](https://recallrai.com) or the source code repository on [GitHub](https://github.com/recallrai/sdk-python).
