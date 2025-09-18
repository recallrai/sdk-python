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
from recallrai.exceptions import UserAlreadyExistsError
try:
    user = client.create_user(user_id="user123", metadata={"name": "John Doe"})
    print(f"Created user: {user.user_id}")
    print(f"User metadata: {user.metadata}")
    print(f"Created at: {user.created_at}")
except UserAlreadyExistsError as e:
    print(f"Error: {e}")
```

### Get a User

```python
from recallrai.exceptions import UserNotFoundError
try:
    user = client.get_user("user123")
    print(f"User metadata: {user.metadata}")
    print(f"Last active: {user.last_active_at}")
except UserNotFoundError as e:
    print(f"Error: {e}")
```

### List Users

```python
user_list = client.list_users(offset=0, limit=10, metadata_filter={"role": "admin"})
print(f"Total users: {user_list.total}")
print(f"Has more users: {user_list.has_more}")

for user in user_list.users:
    print(f"User ID: {user.user_id}")
    print(f"Metadata: {user.metadata}")
    print(f"Created at: {user.created_at}")
    print(f"Last active: {user.last_active_at}")
    print("---")
```

### Update a User

```python
from recallrai.exceptions import UserNotFoundError, UserAlreadyExistsError
try:
    user = client.get_user("user123")
    updated_user = user.update(
        new_metadata={"name": "John Doe", "role": "admin"},
        new_user_id="john_doe"
    )
    print(f"Updated user ID: {updated_user.user_id}")
    print(f"Updated metadata: {updated_user.metadata}")
except UserNotFoundError as e:
    print(f"Error: {e}")
except UserAlreadyExistsError as e:
    print(f"Error: {e}")
```

### Delete a User

```python
from recallrai.exceptions import UserNotFoundError
try:
    user = client.get_user("john_doe")
    user.delete()
    print("User deleted successfully")
except UserNotFoundError as e:
    print(f"Error: {e}")
```

## Session Management

### Create a Session

```python
from recallrai.exceptions import UserNotFoundError
from recallrai.session import Session

try:
    # First, get the user
    user = client.get_user("user123")
    
    # Create a session for the user.
    session: Session = user.create_session(
        auto_process_after_seconds=600,
        metadata={"type": "chat"}
    )
    print("Created session id:", session.session_id)
except UserNotFoundError as e:
    print(f"Error: {e}")
```

### Get an Existing Session

```python
from recallrai.exceptions import UserNotFoundError, SessionNotFoundError

try:
    # First, get the user
    user = client.get_user("user123")
    
    # Retrieve an existing session by its ID
    session = user.get_session(session_id="session-uuid")
    print("Session status:", session.get_status())
except UserNotFoundError as e:
    print(f"Error: {e}")
except SessionNotFoundError as e:
    print(f"Error: {e}")
```

### List Sessions

```python
from recallrai.exceptions import UserNotFoundError

try:
    # First, get the user
    user = client.get_user("user123")
    
    # List sessions for this user with optional metadata filters
    session_list = user.list_sessions(
        offset=0,
        limit=10,
        metadata_filter={"type": "chat"},           # optional
        user_metadata_filter={"role": "admin"}       # optional
    )
    for session in session_list.sessions:
        print(session.session_id, session.status, session.metadata)
except UserNotFoundError as e:
    print(f"Error: {e}")
```

<!-- ### Session – Adding Messages

```python
from recallrai.exceptions import UserNotFoundError, SessionNotFoundError, InvalidSessionStateError
from recallrai.models import MessageRole

try:
    # Add a user message
    session.add_message(role=MessageRole.USER, content="Hello! How are you?")
    
    # Add an assistant message
    session.add_message(role=MessageRole.ASSISTANT, content="I'm an assistant. How can I help you?")
except UserNotFoundError as e:
    print(f"Error: {e}")
except SessionNotFoundError as e:
    print(f"Error: {e}")
except InvalidSessionStateError as e:
    print(f"Error: {e}")
``` -->

<!-- ### Session – Retrieving Context

```python
from recallrai.exceptions import UserNotFoundError, SessionNotFoundError

try:
    context = session.get_context()
    print("Memory used:", context.memory_used)
    print("Context:", context.context)
except UserNotFoundError as e:
    print(f"Error: {e}")
except SessionNotFoundError as e:
    print(f"Error: {e}")
``` -->

### Session – Process Session

```python
from recallrai.exceptions import UserNotFoundError, SessionNotFoundError, InvalidSessionStateError

try:
    session.process()
except UserNotFoundError as e:
    print(f"Error: {e}")
except SessionNotFoundError as e:
    print(f"Error: {e}")
except InvalidSessionStateError as e:
    print(f"Error: {e}")
```

### Session – Getting Status

```python
from recallrai.exceptions import UserNotFoundError, SessionNotFoundError

try:
    status = session.get_status()
    print("Session status:", status)
except UserNotFoundError as e:
    print(f"Error: {e}")
except SessionNotFoundError as e:
    print(f"Error: {e}")
```

### Session – List Messages

```python
from recallrai.exceptions import UserNotFoundError, SessionNotFoundError

try:
    messages = session.get_messages()
    for msg in messages:
        print(f"{msg.role.capitalize()}:(at {msg.timestamp}): {msg.content}")
except UserNotFoundError as e:
    print(f"Error: {e}")
except SessionNotFoundError as e:
    print(f"Error: {e}")
```

## User Memories

### List User Memories (with optional category filters)

```python
from recallrai.exceptions import UserNotFoundError

try:
    user = client.get_user("user123")
    memories = user.list_memories(
        categories=["food_preferences", "alergies"],  # optional
        offset=0,
        limit=20,
    )
    for mem in memories.items:
        print(f"Memory ID: {mem.memory_id}")
        print(f"Categories: {mem.categories}")
        print(f"Content: {mem.content}")
        print(f"Created at: {mem.created_at}")
        print("---")
    print(f"Has more?: {memories.has_more}")
    print(f"Total memories: {memories.total}")
except UserNotFoundError as e:
    print(f"Error: {e}")
```

<!-- ## Example Usage with LLMs

```python
import openai
from recallrai import RecallrAI
from recallrai.exceptions import UserNotFoundError

# Initialize RecallrAI and OpenAI clients
rai_client = RecallrAI(
    api_key="rai_yourapikey", 
    project_id="your-project-uuid"
)
oai_client = openai.OpenAI(api_key="your-openai-api-key")

def chat_with_memory(user_id, session_id=None):
    # Get or create user
    try:
        user = rai_client.get_user(user_id)
    except UserNotFoundError:
        user = rai_client.create_user(user_id)
    
    # Create a new session or get an existing one
    if session_id:
        session = user.get_session(session_id=session_id)
    else:
        session = user.create_session(auto_process_after_minutes=30)
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

        # Call the LLM with the system prompt and conversation history
        response = oai_client.chat.completions.create(
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
``` -->

## Exception Handling

The RecallrAI SDK implements a comprehensive exception hierarchy to help you handle different error scenarios gracefully:

### Base Exception

- **RecallrAIError**: The base exception for all SDK-specific errors. All other exceptions inherit from this.

### Authentication Errors

- **AuthenticationError**: Raised when there's an issue with your API key or project ID authentication.

### Network-Related Errors

- **NetworkError**: Base exception for all network-related issues.
- **TimeoutError**: Occurs when a request takes too long to complete.
- **ConnectionError**: Happens when the SDK cannot establish a connection to the RecallrAI API.

### Server Errors

- **ServerError**: Base class for server-side errors.
- **InternalServerError**: Raised when the RecallrAI API returns a 5xx error code.

### User-Related Errors

- **UserError**: Base for all user-related exceptions.
- **UserNotFoundError**: Raised when attempting to access a user that doesn't exist.
- **UserAlreadyExistsError**: Occurs when creating a user with an ID that already exists.

### Session-Related Errors

- **SessionError**: Base for all session-related exceptions.
- **SessionNotFoundError**: Raised when attempting to access a non-existent session.
- **InvalidSessionStateError**: Occurs when performing an operation that's not valid for the current session state (e.g., adding a message to a processed session).

### Input Validation Errors

- **ValidationError**: Raised when provided data doesn't meet the required format or constraints.

### Importing Exceptions

You can import exceptions directly from the `recallrai.exceptions` module:

```python
# Import specific exceptions
from recallrai.exceptions import UserNotFoundError, SessionNotFoundError

# Import all exceptions
from recallrai.exceptions import (
    RecallrAIError,
    AuthenticationError,
    NetworkError,
    TimeoutError,
    ConnectionError,
    ServerError, 
    InternalServerError,
    SessionError, 
    SessionNotFoundError, 
    InvalidSessionStateError,
    UserError, 
    UserNotFoundError, 
    UserAlreadyExistsError,
    ValidationError,
)
```

### Best Practices for Error Handling

When implementing error handling with the RecallrAI SDK, consider these best practices:

1. **Handle specific exceptions first**: Catch more specific exceptions before general ones.

   ```python
   try:
       # SDK operation
   except UserNotFoundError:
       # Specific handling
   except RecallrAIError:
       # General fallback
   ```

2. **Implement retry logic for transient errors**: Network and timeout errors might be temporary.

3. **Log detailed error information**: Exceptions contain useful information for debugging.

4. **Handle common user flows**: For example, check if a user exists before operations, or create them if they don't:

   ```python
   try:
       user = client.get_user(user_id)
   except UserNotFoundError:
       user = client.create_user(user_id)
   ```

For more detailed information on specific exceptions, refer to the API documentation.

## Conclusion

This README outlines the basic usage of the RecallrAI SDK functions for user and session management. For additional documentation and advanced usage, please see the [official documentation](https://recallrai.com) or the source code repository on [GitHub](https://github.com/recallrai/sdk-python).
