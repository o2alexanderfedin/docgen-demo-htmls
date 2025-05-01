# Prompt Execution API

The Prompt Execution API allows you to execute prompts against LLM providers.

## Table of Contents

- [Overview](#overview)
- [Execute Chat Prompt](#execute-chat-prompt)
- [Execute Prompt](#execute-prompt)
- [Infer Prompt](#infer-prompt)
- [Execute Direct Prompt](#execute-direct-prompt)
- [Stream Response](#stream-response)

## Overview

The Prompt Execution API supports several modes of interaction with LLMs:

- **Chat Completion**: For conversational interactions with the LLM
- **Text Completion**: For traditional prompt-based interactions
- **Streaming**: For real-time responses from the LLM
- **Direct Execution**: For executing prompts directly without pre-registration

## Execute Chat Prompt

Executes a chat-style prompt against the specified LLM provider.

### Endpoint

```
POST /llm/v1/execution/fetchChatAnswer
```

### Permission

`llm:execute`

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |
| promptName | string | Yes | The name of the prompt to execute |
| requestParams | array | No | Array of parameters to apply to the prompt |
| messages | array | No | Array of chat messages for conversation context |
| config | object | No | Configuration overrides for this request |
| isDebug | boolean | No | Whether to include debug information in the response |
| botId | number | No | The ID of the bot (if applicable) |
| useCache | boolean | No | Whether to use cached responses if available |
| enableFunctionCalling | boolean | No | Whether to enable function calling capabilities |
| functionDefinitions | array | No | Array of function definitions for function calling |

#### requestParams Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | The name of the parameter |
| value | any | Yes | The value of the parameter |

#### messages Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| role | string | Yes | The role of the message sender (system, user, assistant) |
| content | string | Yes | The content of the message |
| contentType | string | No | The type of content (TEXT, IMAGE, FUNCTION_CALL) |
| function_call | object | No | Function call information (if applicable) |

#### config Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| temperature | number | No | Sampling temperature (0-1) |
| maxTokens | number | No | Maximum tokens to generate |
| stopSequences | array | No | Array of stop sequences |
| topP | number | No | Top-p sampling value |
| topK | number | No | Top-k sampling value |
| presencePenalty | number | No | Presence penalty |
| frequencyPenalty | number | No | Frequency penalty |
| provider | string | No | Override the LLM provider |
| model | string | No | Override the model to use |

### Response Parameters

| Field | Type | Description |
|-------|------|-------------|
| statusCode | number | HTTP status code |
| message | string | The generated response message |
| responseParams | object | Output parameters extracted from the response |
| errorMessage | string | Error message (if applicable) |
| errorCode | string | Error code (if applicable) |
| llmDebugInfos | array | Debug information (if isDebug=true) |

### Example

#### Request

```bash
curl -X POST https://api.aisera.com/llm/v1/execution/fetchChatAnswer \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tenantId": "9000",
    "promptName": "customer-support-qa",
    "requestParams": [
      {
        "name": "query",
        "value": "How do I reset my password?"
      }
    ],
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful customer support assistant."
      },
      {
        "role": "user",
        "content": "How do I reset my password?"
      }
    ],
    "config": {
      "temperature": 0.7,
      "maxTokens": 500
    },
    "botId": 123,
    "useCache": true
  }'
```

#### Python Example

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com/llm/v1"

payload = {
    "tenantId": "9000",
    "promptName": "customer-support-qa",
    "requestParams": [
        {
            "name": "query",
            "value": "How do I reset my password?"
        }
    ],
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful customer support assistant."
        },
        {
            "role": "user",
            "content": "How do I reset my password?"
        }
    ],
    "config": {
        "temperature": 0.7,
        "maxTokens": 500
    },
    "botId": 123,
    "useCache": True
}

response = requests.post(
    f"{base_url}/execution/fetchChatAnswer",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json=payload
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

#### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const apiKey = 'YOUR_API_KEY';
const baseUrl = 'https://api.aisera.com/llm/v1';

async function executeChatPrompt() {
  try {
    const payload = {
      tenantId: '9000',
      promptName: 'customer-support-qa',
      requestParams: [
        {
          name: 'query',
          value: 'How do I reset my password?'
        }
      ],
      messages: [
        {
          role: 'system',
          content: 'You are a helpful customer support assistant.'
        },
        {
          role: 'user',
          content: 'How do I reset my password?'
        }
      ],
      config: {
        temperature: 0.7,
        maxTokens: 500
      },
      botId: 123,
      useCache: true
    };
    
    const response = await axios.post(
      `${baseUrl}/execution/fetchChatAnswer`,
      payload,
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    console.log(`Status: ${response.status}`);
    console.log(`Response: ${JSON.stringify(response.data)}`);
  } catch (error) {
    console.error('Error executing chat prompt:', error.message);
  }
}

executeChatPrompt();
```

#### Response

```json
{
  "statusCode": 200,
  "message": "To reset your password, follow these steps:\n\n1. Go to the login page\n2. Click on 'Forgot Password' link\n3. Enter your email address\n4. Check your email for a password reset link\n5. Click the link and follow the instructions to create a new password\n\nIf you don't receive the email within a few minutes, check your spam folder or contact our support team for further assistance.",
  "responseParams": {
    "answer": "To reset your password, follow these steps:\n\n1. Go to the login page\n2. Click on 'Forgot Password' link\n3. Enter your email address\n4. Check your email for a password reset link\n5. Click the link and follow the instructions to create a new password\n\nIf you don't receive the email within a few minutes, check your spam folder or contact our support team for further assistance.",
    "category": "password-reset"
  }
}
```

### Error Response

```json
{
  "statusCode": 404,
  "errorMessage": "Prompt 'customer-support-qa' not found in tenant '9000' for bot '123'",
  "errorCode": "PROMPT_NOT_FOUND"
}
```

## Execute Prompt

Executes a non-conversational prompt against the specified LLM provider.

### Endpoint

```
POST /llm/v1/execution/fetchAnswer
```

### Permission

`llm:execute`

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |
| promptName | string | Yes | The name of the prompt to execute |
| requestParams | array | No | Array of parameters to apply to the prompt |
| config | object | No | Configuration overrides for this request |
| isDebug | boolean | No | Whether to include debug information in the response |
| botId | number | No | The ID of the bot (if applicable) |
| useCache | boolean | No | Whether to use cached responses if available |

### Response Parameters

| Field | Type | Description |
|-------|------|-------------|
| statusCode | number | HTTP status code |
| responseParams | array | Output parameters extracted from the response |
| errorMessage | string | Error message (if applicable) |
| llmDebugInfos | array | Debug information (if isDebug=true) |

### Example

#### Request

```bash
curl -X POST https://api.aisera.com/llm/v1/execution/fetchAnswer \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tenantId": "9000",
    "promptName": "text-summarization",
    "requestParams": [
      {
        "name": "text",
        "value": "The quick brown fox jumps over the lazy dog. It was a bright and sunny day in the forest. The animals were all going about their business."
      }
    ],
    "config": {
      "temperature": 0.3,
      "maxTokens": 100
    },
    "botId": 123,
    "useCache": true
  }'
```

#### Python Example

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com/llm/v1"

payload = {
    "tenantId": "9000",
    "promptName": "text-summarization",
    "requestParams": [
        {
            "name": "text",
            "value": "The quick brown fox jumps over the lazy dog. It was a bright and sunny day in the forest. The animals were all going about their business."
        }
    ],
    "config": {
        "temperature": 0.3,
        "maxTokens": 100
    },
    "botId": 123,
    "useCache": True
}

response = requests.post(
    f"{base_url}/execution/fetchAnswer",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json=payload
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

#### Response

```json
{
  "statusCode": 200,
  "responseParams": [
    {
      "name": "summary",
      "value": "A fox jumps over a dog on a sunny day in the forest while animals are active."
    }
  ]
}
```

## Infer Prompt

Retrieves information about a prompt for execution.

### Endpoint

```
POST /llm/v1/execution/inferPrompt
```

### Permission

`llm:read`

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |
| promptName | string | Yes | The name of the prompt |
| botId | number | No | The ID of the bot (if applicable) |

### Response Parameters

Returns the prompt and prompt group information.

### Example

#### Request

```bash
curl -X POST https://api.aisera.com/llm/v1/execution/inferPrompt?tenantId=9000&promptName=customer-support-qa&botId=123 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Response

```json
{
  "prompt": {
    "id": 456,
    "name": "customer-support-qa",
    "displayName": "Customer Support Q&A",
    "template": "You are a helpful customer support assistant. Answer the following question:\n\n{{query}}",
    "userTemplate": "{{query}}",
    "inputParams": [
      {
        "name": "query",
        "type": "string",
        "required": true,
        "description": "The user's question"
      }
    ],
    "outputParams": [
      {
        "name": "answer",
        "type": "string",
        "description": "The answer to the question"
      },
      {
        "name": "category",
        "type": "string",
        "description": "The category of the question"
      }
    ],
    "llmRegistryId": 789,
    "botId": 123
  },
  "promptGroup": {
    "id": 789,
    "name": "gpt-4",
    "displayName": "GPT-4",
    "description": "OpenAI's GPT-4 model",
    "endpoint": "https://api.openai.com/v1/chat/completions",
    "config": {
      "provider": "openai",
      "model": "gpt-4"
    }
  },
  "tenantUtilized": "9000"
}
```

## Execute Direct Prompt

Executes a prompt directly without requiring pre-registration.

### Endpoint

```
POST /v1/tenants/{tenantId}/llm/prompts/execute
```

### Permission

`llm:execute`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| modelId | number | Yes | The ID of the LLM model to use |
| promptText | string | Yes | The prompt text to execute |
| inputs | object | No | Input values for variables in the prompt |
| config | object | No | Configuration overrides for this request |

### Response Parameters

| Field | Type | Description |
|-------|------|-------------|
| output | string | The generated response |
| status | string | Status of the execution |

### Example

#### Request

```bash
curl -X POST https://api.aisera.com/v1/tenants/9000/llm/prompts/execute \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "modelId": 789,
    "promptText": "Summarize the following text in one sentence: {{text}}",
    "inputs": {
      "text": "The quick brown fox jumps over the lazy dog. It was a bright and sunny day in the forest. The animals were all going about their business."
    },
    "config": {
      "temperature": 0.3,
      "maxTokens": 100
    }
  }'
```

#### Response

```json
{
  "output": "A fox jumps over a dog on a sunny day in the forest while animals are active.",
  "status": "success"
}
```

## Stream Response

Streams the response from the LLM in real-time.

### Endpoint

```
POST /llm/v1/execution/stream
```

### Permission

`llm:execute`

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |
| promptName | string | Yes | The name of the prompt to execute |
| requestParams | array | No | Array of parameters to apply to the prompt |
| messages | array | No | Array of chat messages for conversation context |
| config | object | No | Configuration overrides for this request |
| botId | number | No | The ID of the bot (if applicable) |

### Response

The server sends a stream of Server-Sent Events (SSE), each containing a chunk of the response.

### Example

#### Request

```bash
curl -X POST https://api.aisera.com/llm/v1/execution/stream \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tenantId": "9000",
    "promptName": "customer-support-qa",
    "requestParams": [
      {
        "name": "query",
        "value": "How do I reset my password?"
      }
    ],
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful customer support assistant."
      },
      {
        "role": "user",
        "content": "How do I reset my password?"
      }
    ],
    "config": {
      "temperature": 0.7,
      "maxTokens": 500
    },
    "botId": 123
  }'
```

#### Python Example

```python
import requests
import sseclient

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com/llm/v1"

payload = {
    "tenantId": "9000",
    "promptName": "customer-support-qa",
    "requestParams": [
        {
            "name": "query",
            "value": "How do I reset my password?"
        }
    ],
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful customer support assistant."
        },
        {
            "role": "user",
            "content": "How do I reset my password?"
        }
    ],
    "config": {
        "temperature": 0.7,
        "maxTokens": 500
    },
    "botId": 123
}

response = requests.post(
    f"{base_url}/execution/stream",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    },
    json=payload,
    stream=True
)

client = sseclient.SSEClient(response)
for event in client.events():
    print(f"Received: {event.data}")
```

#### JavaScript/Node.js Example

```javascript
const EventSource = require('eventsource');
const fetch = require('node-fetch');

const apiKey = 'YOUR_API_KEY';
const baseUrl = 'https://api.aisera.com/llm/v1';

async function streamResponse() {
  try {
    const payload = {
      tenantId: '9000',
      promptName: 'customer-support-qa',
      requestParams: [
        {
          name: 'query',
          value: 'How do I reset my password?'
        }
      ],
      messages: [
        {
          role: 'system',
          content: 'You are a helpful customer support assistant.'
        },
        {
          role: 'user',
          content: 'How do I reset my password?'
        }
      ],
      config: {
        temperature: 0.7,
        maxTokens: 500
      },
      botId: 123
    };
    
    const response = await fetch(`${baseUrl}/execution/stream`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
    
    // Get the response URL for EventSource
    const streamUrl = response.url;
    
    const eventSource = new EventSource(streamUrl, {
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    });
    
    eventSource.onmessage = (event) => {
      console.log(`Received: ${event.data}`);
      
      // Check if this is the last message
      const data = JSON.parse(event.data);
      if (data.is_done) {
        eventSource.close();
      }
    };
    
    eventSource.onerror = (error) => {
      console.error('EventSource error:', error);
      eventSource.close();
    };
  } catch (error) {
    console.error('Error setting up stream:', error.message);
  }
}

streamResponse();
```

#### Response Stream (SSE)

```
data: {"content":"To reset your ", "is_done": false}

data: {"content":"password, follow ", "is_done": false}

data: {"content":"these steps:", "is_done": false}

data: {"content":"\n\n1. Go to the login page", "is_done": false}

data: {"content":"\n2. Click on 'Forgot Password' link", "is_done": false}

data: {"content":"\n3. Enter your email address", "is_done": false}

data: {"content":"\n4. Check your email for a password reset link", "is_done": false}

data: {"content":"\n5. Click the link and follow the instructions to create a new password", "is_done": false}

data: {"content":"\n\nIf you don't receive the email within a few minutes, check your spam folder or contact our support team for further assistance.", "is_done": true}
```