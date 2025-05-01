# LLM Registry API

The LLM Registry API allows you to manage LLM provider configurations and retrieve information about available models.

## Table of Contents

- [Overview](#overview)
- [List Models](#list-models)
- [List Providers](#list-providers)
- [List Categories](#list-categories)

## Overview

The LLM Registry API provides endpoints for retrieving information about the available LLM models and providers. This information is useful for configuring prompts and selecting the appropriate LLM for different use cases.

## List Models

Retrieves a list of available LLM models for a tenant.

### Endpoint

```
GET /v1/tenants/{tenantId}/llm/prompts/models
```

### Permission

`llm:read`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |

### Response Parameters

Returns an array of LLM model objects.

### Example

#### Request

```bash
curl -X GET "https://api.aisera.com/v1/tenants/9000/llm/prompts/models" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Python Example

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com"
tenant_id = "9000"

response = requests.get(
    f"{base_url}/v1/tenants/{tenant_id}/llm/prompts/models",
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

#### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const apiKey = 'YOUR_API_KEY';
const baseUrl = 'https://api.aisera.com';
const tenantId = '9000';

async function listModels() {
  try {
    const response = await axios.get(
      `${baseUrl}/v1/tenants/${tenantId}/llm/prompts/models`,
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`
        }
      }
    );
    
    console.log(`Status: ${response.status}`);
    console.log(`Response: ${JSON.stringify(response.data)}`);
  } catch (error) {
    console.error('Error listing models:', error.message);
  }
}

listModels();
```

#### Response

```json
[
  {
    "id": 1,
    "name": "gpt-4",
    "displayName": "GPT-4",
    "description": "OpenAI's most capable model, optimized for chat",
    "contextWindow": 8192,
    "cost": {
      "inputTokens": 0.03,
      "outputTokens": 0.06,
      "unit": "USD per 1000 tokens"
    },
    "capabilities": [
      "text-generation",
      "chat",
      "function-calling"
    ]
  },
  {
    "id": 2,
    "name": "llama2-70b",
    "displayName": "Llama 2 (70B)",
    "description": "Meta's open source large language model",
    "contextWindow": 4096,
    "cost": {
      "inputTokens": 0.00075,
      "outputTokens": 0.00075,
      "unit": "USD per 1000 tokens"
    },
    "capabilities": [
      "text-generation",
      "chat"
    ]
  }
]
```

## List Providers

Retrieves a list of available LLM providers for a tenant.

### Endpoint

```
GET /v1/tenants/{tenantId}/llm/prompts/providers
```

### Permission

`llm:read`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |

### Response Parameters

Returns an array of provider names.

### Example

#### Request

```bash
curl -X GET "https://api.aisera.com/v1/tenants/9000/llm/prompts/providers" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Response

```json
[
  "openai",
  "bedrock",
  "anthropic",
  "aisera"
]
```

## List Categories

Retrieves a list of available prompt categories for a tenant.

### Endpoint

```
GET /v1/tenants/{tenantId}/llm/prompts/categories
```

### Permission

`llm:read`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |

### Response Parameters

Returns an array of category names.

### Example

#### Request

```bash
curl -X GET "https://api.aisera.com/v1/tenants/9000/llm/prompts/categories" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Python Example

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com"
tenant_id = "9000"

response = requests.get(
    f"{base_url}/v1/tenants/{tenant_id}/llm/prompts/categories",
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

#### Response

```json
[
  "support",
  "summarization",
  "extraction",
  "classification",
  "generation"
]
```