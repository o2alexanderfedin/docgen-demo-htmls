# Prompt Management API

The Prompt Management API allows you to create, read, update, and delete prompts and prompt groups.

## Table of Contents

- [Overview](#overview)
- [Prompt Groups](#prompt-groups)
  - [List Prompt Groups](#list-prompt-groups)
  - [Get Prompt Group](#get-prompt-group)
  - [Create Prompt Group](#create-prompt-group)
  - [Update Prompt Group](#update-prompt-group)
  - [Delete Prompt Group](#delete-prompt-group)
- [Prompts](#prompts)
  - [List Prompts](#list-prompts)
  - [List Prompts by Tenant](#list-prompts-by-tenant)
  - [Get Prompt](#get-prompt)
  - [Create Prompt](#create-prompt)
  - [Update Prompt](#update-prompt)
  - [Delete Prompt](#delete-prompt)

## Overview

The Prompt Management API is divided into two main areas:

1. **Prompt Groups**: Collections of prompts that share common configurations like LLM provider details
2. **Prompts**: Individual prompt templates with input and output parameter definitions

## Prompt Groups

### List Prompt Groups

Retrieves a list of all prompt groups for a tenant.

#### Endpoint

```
GET /llm/v1/prompt_group/list
```

#### Permission

`llm:read`

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | No | The ID of the tenant (defaults to "9000") |
| showTenantOnlyGroups | boolean | No | Whether to show only tenant-specific groups (defaults to false) |

#### Response Parameters

Returns an array of prompt group objects.

#### Example

##### Request

```bash
curl -X GET "https://api.aisera.com/llm/v1/prompt_group/list?tenantId=9000" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

##### Python Example

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com/llm/v1"

response = requests.get(
    f"{base_url}/prompt_group/list",
    headers={
        "Authorization": f"Bearer {api_key}"
    },
    params={
        "tenantId": "9000"
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

##### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const apiKey = 'YOUR_API_KEY';
const baseUrl = 'https://api.aisera.com/llm/v1';

async function listPromptGroups() {
  try {
    const response = await axios.get(
      `${baseUrl}/prompt_group/list`,
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`
        },
        params: {
          tenantId: '9000'
        }
      }
    );
    
    console.log(`Status: ${response.status}`);
    console.log(`Response: ${JSON.stringify(response.data)}`);
  } catch (error) {
    console.error('Error listing prompt groups:', error.message);
  }
}

listPromptGroups();
```

##### Response

```json
[
  {
    "id": 1,
    "name": "gpt-4",
    "displayName": "GPT-4",
    "description": "OpenAI's GPT-4 model",
    "category": "openai",
    "isActive": true,
    "endpoint": "https://api.openai.com/v1/chat/completions",
    "config": {
      "provider": "openai",
      "model": "gpt-4"
    },
    "authConfig": {
      "apiKeyHeader": "Authorization",
      "apiKeyPrefix": "Bearer "
    }
  },
  {
    "id": 2,
    "name": "llama2",
    "displayName": "Llama 2",
    "description": "Meta's Llama 2 model via AWS Bedrock",
    "category": "bedrock",
    "isActive": true,
    "endpoint": "https://bedrock.aws.amazon.com/model/llama2-70b",
    "config": {
      "provider": "bedrock",
      "model": "llama2-70b"
    },
    "authConfig": {
      "authType": "aws_signature"
    }
  }
]
```

### Get Prompt Group

Retrieves a specific prompt group by name.

#### Endpoint

```
GET /llm/v1/prompt_group
```

#### Permission

`llm:read`

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | No | The ID of the tenant (defaults to "9000") |
| name | string | Yes | The name of the prompt group |
| showTenantOnlyGroups | boolean | No | Whether to show only tenant-specific groups (defaults to false) |

#### Response Parameters

Returns the prompt group object.

#### Example

##### Request

```bash
curl -X GET "https://api.aisera.com/llm/v1/prompt_group?tenantId=9000&name=gpt-4" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

##### Response

```json
{
  "id": 1,
  "name": "gpt-4",
  "displayName": "GPT-4",
  "description": "OpenAI's GPT-4 model",
  "category": "openai",
  "isActive": true,
  "endpoint": "https://api.openai.com/v1/chat/completions",
  "config": {
    "provider": "openai",
    "model": "gpt-4"
  },
  "authConfig": {
    "apiKeyHeader": "Authorization",
    "apiKeyPrefix": "Bearer "
  }
}
```

### Create Prompt Group

Creates a new prompt group.

#### Endpoint

```
POST /llm/v1/prompt_group
```

#### Permission

`llm:write`

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | No | The ID of the tenant (defaults to "9000") |

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | The name of the prompt group |
| displayName | string | No | The display name of the prompt group |
| description | string | No | The description of the prompt group |
| category | string | No | The category of the prompt group |
| isActive | boolean | No | Whether the prompt group is active |
| endpoint | string | Yes | The endpoint for the LLM provider |
| config | object | No | Configuration for the LLM provider |
| authConfig | object | No | Authentication configuration for the LLM provider |

#### Response Parameters

Returns the created prompt group object.

#### Example

##### Request

```bash
curl -X POST "https://api.aisera.com/llm/v1/prompt_group?tenantId=9000" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "claude-instant",
    "displayName": "Claude Instant",
    "description": "Anthropic's Claude Instant model",
    "category": "anthropic",
    "isActive": true,
    "endpoint": "https://api.anthropic.com/v1/messages",
    "config": {
      "provider": "anthropic",
      "model": "claude-instant-1.2"
    },
    "authConfig": {
      "apiKeyHeader": "x-api-key"
    }
  }'
```

##### Python Example

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com/llm/v1"

payload = {
    "name": "claude-instant",
    "displayName": "Claude Instant",
    "description": "Anthropic's Claude Instant model",
    "category": "anthropic",
    "isActive": True,
    "endpoint": "https://api.anthropic.com/v1/messages",
    "config": {
      "provider": "anthropic",
      "model": "claude-instant-1.2"
    },
    "authConfig": {
      "apiKeyHeader": "x-api-key"
    }
}

response = requests.post(
    f"{base_url}/prompt_group",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    params={
        "tenantId": "9000"
    },
    json=payload
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

##### Response

```json
{
  "id": 3,
  "name": "claude-instant",
  "displayName": "Claude Instant",
  "description": "Anthropic's Claude Instant model",
  "category": "anthropic",
  "isActive": true,
  "endpoint": "https://api.anthropic.com/v1/messages",
  "config": {
    "provider": "anthropic",
    "model": "claude-instant-1.2"
  },
  "authConfig": {
    "apiKeyHeader": "x-api-key"
  }
}
```

### Update Prompt Group

Updates an existing prompt group.

#### Endpoint

```
PUT /llm/v1/prompt_group
```

#### Permission

`llm:write`

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | No | The ID of the tenant (defaults to "9000") |

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | The name of the prompt group (cannot be changed) |
| displayName | string | No | The display name of the prompt group |
| description | string | No | The description of the prompt group |
| category | string | No | The category of the prompt group |
| isActive | boolean | No | Whether the prompt group is active |
| endpoint | string | No | The endpoint for the LLM provider |
| config | object | No | Configuration for the LLM provider |
| authConfig | object | No | Authentication configuration for the LLM provider |

#### Response Parameters

Returns the updated prompt group object.

#### Example

##### Request

```bash
curl -X PUT "https://api.aisera.com/llm/v1/prompt_group?tenantId=9000" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "claude-instant",
    "displayName": "Claude Instant Updated",
    "description": "Anthropic's Claude Instant model - updated description",
    "config": {
      "provider": "anthropic",
      "model": "claude-instant-1.2",
      "maxTokens": 2000
    }
  }'
```

##### Response

```json
{
  "id": 3,
  "name": "claude-instant",
  "displayName": "Claude Instant Updated",
  "description": "Anthropic's Claude Instant model - updated description",
  "category": "anthropic",
  "isActive": true,
  "endpoint": "https://api.anthropic.com/v1/messages",
  "config": {
    "provider": "anthropic",
    "model": "claude-instant-1.2",
    "maxTokens": 2000
  },
  "authConfig": {
    "apiKeyHeader": "x-api-key"
  }
}
```

### Delete Prompt Group

Deletes a prompt group. Note that a prompt group can only be deleted if it has no associated prompts.

#### Endpoint

```
DELETE /llm/v1/prompt_group
```

#### Permission

`llm:delete`

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | No | The ID of the tenant (defaults to "9000") |
| name | string | Yes | The name of the prompt group |

#### Response Parameters

Returns a 200 OK status if successful.

#### Example

##### Request

```bash
curl -X DELETE "https://api.aisera.com/llm/v1/prompt_group?tenantId=9000&name=claude-instant" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

##### Response

```
200 OK
```

## Prompts

### List Prompts

Retrieves a list of prompts for a prompt group or bot.

#### Endpoint

```
GET /llm/v1/prompt/list
```

#### Permission

`llm:read`

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | No | The ID of the tenant (defaults to "9000") |
| groupId | number | No | The ID of the prompt group |
| showTenantOnlyPrompts | boolean | No | Whether to show only tenant-specific prompts (defaults to false) |

#### Response Parameters

Returns an array of prompt objects.

#### Example

##### Request

```bash
curl -X GET "https://api.aisera.com/llm/v1/prompt/list?tenantId=9000&groupId=1" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

##### Python Example

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com/llm/v1"

response = requests.get(
    f"{base_url}/prompt/list",
    headers={
        "Authorization": f"Bearer {api_key}"
    },
    params={
        "tenantId": "9000",
        "groupId": 1
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

##### Response

```json
[
  {
    "id": 1,
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
    "llmRegistryId": 1,
    "botId": 123,
    "status": "Active",
    "type": "chat",
    "isRegistered": true,
    "isImported": false,
    "isDefault": true,
    "isSystem": false,
    "category": "support",
    "useCase": "Customer support chatbot",
    "script": "function processResponse(response) {\n  return [\n    { name: 'answer', value: response },\n    { name: 'category', value: determineCategory(response) }\n  ];\n}",
    "description": "A prompt for answering customer support questions"
  }
]
```

### List Prompts by Tenant

Retrieves a list of prompts for a tenant.

#### Endpoint

```
GET /v1/tenants/{tenantId}/llm/prompts
```

#### Permission

`llm:read`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| botId | number | No | The ID of the bot |

#### Response Parameters

Returns an array of prompt objects.

#### Example

##### Request

```bash
curl -X GET "https://api.aisera.com/v1/tenants/9000/llm/prompts?botId=123" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

##### Response

```json
[
  {
    "id": 1,
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
    "modelId": 1,
    "botId": 123,
    "status": "Active",
    "scope": "bot",
    "type": "chat",
    "isRegistered": true,
    "isImported": false,
    "isDefault": true,
    "isSystem": false,
    "category": "support",
    "useCase": "Customer support chatbot",
    "script": "function processResponse(response) {\n  return [\n    { name: 'answer', value: response },\n    { name: 'category', value: determineCategory(response) }\n  ];\n}",
    "description": "A prompt for answering customer support questions"
  }
]
```

### Get Prompt

Retrieves a specific prompt by ID.

#### Endpoint

```
GET /v1/tenants/{tenantId}/llm/prompts/{promptId}
```

#### Permission

`llm:read`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |
| promptId | number | Yes | The ID of the prompt |

#### Response Parameters

Returns the prompt object.

#### Example

##### Request

```bash
curl -X GET "https://api.aisera.com/v1/tenants/9000/llm/prompts/1" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

##### Python Example

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com"
tenant_id = "9000"
prompt_id = 1

response = requests.get(
    f"{base_url}/v1/tenants/{tenant_id}/llm/prompts/{prompt_id}",
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

##### Response

```json
{
  "id": 1,
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
  "modelId": 1,
  "botId": 123,
  "status": "Active",
  "scope": "bot",
  "type": "chat",
  "isRegistered": true,
  "isImported": false,
  "isDefault": true,
  "isSystem": false,
  "category": "support",
  "useCase": "Customer support chatbot",
  "script": "function processResponse(response) {\n  return [\n    { name: 'answer', value: response },\n    { name: 'category', value: determineCategory(response) }\n  ];\n}",
  "description": "A prompt for answering customer support questions"
}
```

### Create Prompt

Creates a new prompt.

#### Endpoint

```
POST /v1/tenants/{tenantId}/llm/prompts
```

#### Permission

`llm:write`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| userDetails | string | No | User details for auditing |

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | The name of the prompt |
| displayName | string | No | The display name of the prompt |
| template | string | Yes | The prompt template |
| userTemplate | string | No | The user template portion of the prompt |
| inputParams | array | No | The input parameters for the prompt |
| outputParams | array | No | The output parameters for the prompt |
| modelId | number | Yes | The ID of the LLM model to use |
| botId | number | No | The ID of the bot (if scope is "bot") |
| scope | string | No | The scope of the prompt ("bot", "tenant", or "global") |
| type | string | No | The type of the prompt |
| category | string | No | The category of the prompt |
| useCase | string | No | The use case for the prompt |
| script | string | No | JavaScript script for processing the response |
| description | string | No | The description of the prompt |

#### Response Parameters

Returns the created prompt object.

#### Example

##### Request

```bash
curl -X POST "https://api.aisera.com/v1/tenants/9000/llm/prompts" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "text-summarization",
    "displayName": "Text Summarization",
    "template": "Summarize the following text in one sentence:\n\n{{text}}",
    "inputParams": [
      {
        "name": "text",
        "type": "string",
        "required": true,
        "description": "The text to summarize"
      }
    ],
    "outputParams": [
      {
        "name": "summary",
        "type": "string",
        "description": "The one-sentence summary"
      }
    ],
    "modelId": 1,
    "botId": 123,
    "scope": "bot",
    "type": "completion",
    "category": "summarization",
    "useCase": "Text summarization",
    "script": "function processResponse(response) {\n  return [{ name: \"summary\", value: response.trim() }];\n}",
    "description": "A prompt for summarizing text in one sentence"
  }'
```

##### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const apiKey = 'YOUR_API_KEY';
const baseUrl = 'https://api.aisera.com';
const tenantId = '9000';

async function createPrompt() {
  try {
    const payload = {
      name: 'text-summarization',
      displayName: 'Text Summarization',
      template: 'Summarize the following text in one sentence:\n\n{{text}}',
      inputParams: [
        {
          name: 'text',
          type: 'string',
          required: true,
          description: 'The text to summarize'
        }
      ],
      outputParams: [
        {
          name: 'summary',
          type: 'string',
          description: 'The one-sentence summary'
        }
      ],
      modelId: 1,
      botId: 123,
      scope: 'bot',
      type: 'completion',
      category: 'summarization',
      useCase: 'Text summarization',
      script: 'function processResponse(response) {\n  return [{ name: "summary", value: response.trim() }];\n}',
      description: 'A prompt for summarizing text in one sentence'
    };
    
    const response = await axios.post(
      `${baseUrl}/v1/tenants/${tenantId}/llm/prompts`,
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
    console.error('Error creating prompt:', error.message);
  }
}

createPrompt();
```

##### Response

```json
{
  "id": 2,
  "name": "text-summarization",
  "displayName": "Text Summarization",
  "template": "Summarize the following text in one sentence:\n\n{{text}}",
  "inputParams": [
    {
      "name": "text",
      "type": "string",
      "required": true,
      "description": "The text to summarize"
    }
  ],
  "outputParams": [
    {
      "name": "summary",
      "type": "string",
      "description": "The one-sentence summary"
    }
  ],
  "modelId": 1,
  "botId": 123,
  "status": "Active",
  "scope": "bot",
  "type": "completion",
  "isRegistered": true,
  "isImported": false,
  "isDefault": true,
  "isSystem": false,
  "category": "summarization",
  "useCase": "Text summarization",
  "script": "function processResponse(response) {\n  return [{ name: \"summary\", value: response.trim() }];\n}",
  "description": "A prompt for summarizing text in one sentence"
}
```

### Update Prompt

Updates an existing prompt.

#### Endpoint

```
PUT /v1/tenants/{tenantId}/llm/prompts/{promptId}
```

#### Permission

`llm:write`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |
| promptId | number | Yes | The ID of the prompt |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| userDetails | string | No | User details for auditing |

#### Request Body

Same as the create prompt request body, but the `name` field cannot be changed.

#### Response Parameters

Returns the updated prompt object.

#### Example

##### Request

```bash
curl -X PUT "https://api.aisera.com/v1/tenants/9000/llm/prompts/2" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "Text Summarization Updated",
    "template": "Summarize the following text in one sentence. Be concise and clear:\n\n{{text}}",
    "category": "summarization",
    "script": "function processResponse(response) {\n  return [{ name: \"summary\", value: response.trim() }];\n}"
  }'
```

##### Response

```json
{
  "id": 2,
  "name": "text-summarization",
  "displayName": "Text Summarization Updated",
  "template": "Summarize the following text in one sentence. Be concise and clear:\n\n{{text}}",
  "inputParams": [
    {
      "name": "text",
      "type": "string",
      "required": true,
      "description": "The text to summarize"
    }
  ],
  "outputParams": [
    {
      "name": "summary",
      "type": "string",
      "description": "The one-sentence summary"
    }
  ],
  "modelId": 1,
  "botId": 123,
  "status": "Active",
  "scope": "bot",
  "type": "completion",
  "isRegistered": true,
  "isImported": false,
  "isDefault": true,
  "isSystem": false,
  "category": "summarization",
  "useCase": "Text summarization",
  "script": "function processResponse(response) {\n  return [{ name: \"summary\", value: response.trim() }];\n}",
  "description": "A prompt for summarizing text in one sentence"
}
```

### Delete Prompt

Deletes a prompt.

#### Endpoint

```
DELETE /v1/tenants/{tenantId}/llm/prompts/{promptId}
```

#### Permission

`llm:delete`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |
| promptId | number | Yes | The ID of the prompt |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| userDetails | string | No | User details for auditing |

#### Response Parameters

Returns a 204 No Content status if successful.

#### Example

##### Request

```bash
curl -X DELETE "https://api.aisera.com/v1/tenants/9000/llm/prompts/2?userDetails=jane.doe@example.com" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

##### Response

```
204 No Content
```