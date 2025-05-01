# Prompt Versioning API

The Prompt Versioning API allows you to manage versions of prompts, providing a way to track changes and promote drafts to production.

## Table of Contents

- [Overview](#overview)
- [List Versions](#list-versions)
- [Get Version](#get-version)
- [Create Version](#create-version)
- [Update Version](#update-version)
- [Publish Version](#publish-version)

## Overview

The LLM Gateway supports versioning for prompts, allowing you to create drafts, test changes, and promote versions to production when ready. This ensures a safe workflow for updating prompts without affecting production systems until changes are verified.

Each prompt can have multiple versions with the following states:
- **Draft**: A work-in-progress version that can be modified
- **Published**: An immutable version that's available for use in production
- **Archived**: A previously published version that's no longer in active use

## List Versions

Retrieves all versions of a specific prompt.

### Endpoint

```
GET /v1/tenants/{tenantId}/llm/prompts/{promptId}/versions
```

### Permission

`llm:read`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |
| promptId | string | Yes | The ID of the prompt |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | string | No | Filter by version status (draft, published, archived) |
| page | integer | No | Page number for pagination (default: 1) |
| limit | integer | No | Number of items per page (default: 20, max: 100) |

### Response Parameters

Returns an array of prompt version objects and pagination metadata.

### Example

#### Request

```bash
curl -X GET "https://api.aisera.com/v1/tenants/9000/llm/prompts/pr_123456/versions" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Python Example

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com"
tenant_id = "9000"
prompt_id = "pr_123456"

response = requests.get(
    f"{base_url}/v1/tenants/{tenant_id}/llm/prompts/{prompt_id}/versions",
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

#### Response

```json
{
  "items": [
    {
      "id": "v_abc123",
      "promptId": "pr_123456",
      "version": 3,
      "status": "published",
      "template": "Answer the following question about {{topic}}: {{question}}",
      "parameters": {
        "topic": {
          "type": "string",
          "description": "The topic of the question"
        },
        "question": {
          "type": "string",
          "description": "The question to answer"
        }
      },
      "createdAt": "2023-08-15T14:32:10Z",
      "createdBy": "user@example.com",
      "publishedAt": "2023-08-16T09:45:22Z",
      "publishedBy": "admin@example.com"
    },
    {
      "id": "v_def456",
      "promptId": "pr_123456",
      "version": 2,
      "status": "archived",
      "template": "Please answer this question about {{topic}}: {{question}}",
      "parameters": {
        "topic": {
          "type": "string",
          "description": "The topic of the question"
        },
        "question": {
          "type": "string",
          "description": "The question to answer"
        }
      },
      "createdAt": "2023-07-20T11:22:33Z",
      "createdBy": "user@example.com",
      "publishedAt": "2023-07-21T15:30:00Z",
      "publishedBy": "admin@example.com",
      "archivedAt": "2023-08-16T09:45:22Z",
      "archivedBy": "admin@example.com"
    }
  ],
  "pagination": {
    "total": 3,
    "limit": 20,
    "page": 1,
    "pages": 1
  }
}
```

## Get Version

Retrieves a specific version of a prompt.

### Endpoint

```
GET /v1/tenants/{tenantId}/llm/prompts/{promptId}/versions/{versionId}
```

### Permission

`llm:read`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |
| promptId | string | Yes | The ID of the prompt |
| versionId | string | Yes | The ID of the version |

### Response Parameters

Returns a prompt version object.

### Example

#### Request

```bash
curl -X GET "https://api.aisera.com/v1/tenants/9000/llm/prompts/pr_123456/versions/v_abc123" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const apiKey = 'YOUR_API_KEY';
const baseUrl = 'https://api.aisera.com';
const tenantId = '9000';
const promptId = 'pr_123456';
const versionId = 'v_abc123';

async function getVersion() {
  try {
    const response = await axios.get(
      `${baseUrl}/v1/tenants/${tenantId}/llm/prompts/${promptId}/versions/${versionId}`,
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`
        }
      }
    );
    
    console.log(`Status: ${response.status}`);
    console.log(`Response: ${JSON.stringify(response.data, null, 2)}`);
  } catch (error) {
    console.error('Error getting version:', error.message);
  }
}

getVersion();
```

#### Response

```json
{
  "id": "v_abc123",
  "promptId": "pr_123456",
  "version": 3,
  "status": "published",
  "template": "Answer the following question about {{topic}}: {{question}}",
  "parameters": {
    "topic": {
      "type": "string",
      "description": "The topic of the question"
    },
    "question": {
      "type": "string",
      "description": "The question to answer"
    }
  },
  "createdAt": "2023-08-15T14:32:10Z",
  "createdBy": "user@example.com",
  "publishedAt": "2023-08-16T09:45:22Z",
  "publishedBy": "admin@example.com"
}
```

## Create Version

Creates a new draft version of a prompt.

### Endpoint

```
POST /v1/tenants/{tenantId}/llm/prompts/{promptId}/versions
```

### Permission

`llm:write`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |
| promptId | string | Yes | The ID of the prompt |

### Request Body

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| template | string | Yes | The prompt template with parameter placeholders |
| parameters | object | Yes | A map of parameter definitions |
| defaultModel | string | No | The default LLM model to use |
| description | string | No | A description of this version |

### Response Parameters

Returns the newly created prompt version object.

### Example

#### Request

```bash
curl -X POST "https://api.aisera.com/v1/tenants/9000/llm/prompts/pr_123456/versions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "Answer this {{topic}} question in a {{tone}} tone: {{question}}",
    "parameters": {
      "topic": {
        "type": "string",
        "description": "The topic area of the question",
        "required": true
      },
      "question": {
        "type": "string",
        "description": "The question to answer",
        "required": true
      },
      "tone": {
        "type": "string",
        "description": "The tone to use in the response",
        "enum": ["formal", "casual", "technical"],
        "default": "formal"
      }
    },
    "defaultModel": "gpt-4",
    "description": "Enhanced prompt with tone control"
  }'
```

#### Python Example

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com"
tenant_id = "9000"
prompt_id = "pr_123456"

data = {
    "template": "Answer this {{topic}} question in a {{tone}} tone: {{question}}",
    "parameters": {
        "topic": {
            "type": "string",
            "description": "The topic area of the question",
            "required": True
        },
        "question": {
            "type": "string",
            "description": "The question to answer",
            "required": True
        },
        "tone": {
            "type": "string",
            "description": "The tone to use in the response",
            "enum": ["formal", "casual", "technical"],
            "default": "formal"
        }
    },
    "defaultModel": "gpt-4",
    "description": "Enhanced prompt with tone control"
}

response = requests.post(
    f"{base_url}/v1/tenants/{tenant_id}/llm/prompts/{prompt_id}/versions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json=data
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

#### Response

```json
{
  "id": "v_ghi789",
  "promptId": "pr_123456",
  "version": 4,
  "status": "draft",
  "template": "Answer this {{topic}} question in a {{tone}} tone: {{question}}",
  "parameters": {
    "topic": {
      "type": "string",
      "description": "The topic area of the question",
      "required": true
    },
    "question": {
      "type": "string",
      "description": "The question to answer",
      "required": true
    },
    "tone": {
      "type": "string",
      "description": "The tone to use in the response",
      "enum": ["formal", "casual", "technical"],
      "default": "formal"
    }
  },
  "defaultModel": "gpt-4",
  "description": "Enhanced prompt with tone control",
  "createdAt": "2023-09-01T10:23:45Z",
  "createdBy": "user@example.com"
}
```

## Update Version

Updates a draft version of a prompt. Published versions cannot be updated.

### Endpoint

```
PATCH /v1/tenants/{tenantId}/llm/prompts/{promptId}/versions/{versionId}
```

### Permission

`llm:write`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |
| promptId | string | Yes | The ID of the prompt |
| versionId | string | Yes | The ID of the version |

### Request Body

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| template | string | No | The prompt template with parameter placeholders |
| parameters | object | No | A map of parameter definitions |
| defaultModel | string | No | The default LLM model to use |
| description | string | No | A description of this version |

### Response Parameters

Returns the updated prompt version object.

### Example

#### Request

```bash
curl -X PATCH "https://api.aisera.com/v1/tenants/9000/llm/prompts/pr_123456/versions/v_ghi789" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "Provide an answer about {{topic}} in a {{tone}} tone. Question: {{question}}",
    "description": "Revised enhanced prompt with tone control"
  }'
```

#### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const apiKey = 'YOUR_API_KEY';
const baseUrl = 'https://api.aisera.com';
const tenantId = '9000';
const promptId = 'pr_123456';
const versionId = 'v_ghi789';

const data = {
  template: "Provide an answer about {{topic}} in a {{tone}} tone. Question: {{question}}",
  description: "Revised enhanced prompt with tone control"
};

async function updateVersion() {
  try {
    const response = await axios.patch(
      `${baseUrl}/v1/tenants/${tenantId}/llm/prompts/${promptId}/versions/${versionId}`,
      data,
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    console.log(`Status: ${response.status}`);
    console.log(`Response: ${JSON.stringify(response.data, null, 2)}`);
  } catch (error) {
    console.error('Error updating version:', error.message);
    if (error.response) {
      console.error(`Status: ${error.response.status}`);
      console.error(`Response: ${JSON.stringify(error.response.data, null, 2)}`);
    }
  }
}

updateVersion();
```

#### Response

```json
{
  "id": "v_ghi789",
  "promptId": "pr_123456",
  "version": 4,
  "status": "draft",
  "template": "Provide an answer about {{topic}} in a {{tone}} tone. Question: {{question}}",
  "parameters": {
    "topic": {
      "type": "string",
      "description": "The topic area of the question",
      "required": true
    },
    "question": {
      "type": "string",
      "description": "The question to answer",
      "required": true
    },
    "tone": {
      "type": "string",
      "description": "The tone to use in the response",
      "enum": ["formal", "casual", "technical"],
      "default": "formal"
    }
  },
  "defaultModel": "gpt-4",
  "description": "Revised enhanced prompt with tone control",
  "createdAt": "2023-09-01T10:23:45Z",
  "createdBy": "user@example.com",
  "updatedAt": "2023-09-01T11:05:33Z",
  "updatedBy": "user@example.com"
}
```

## Publish Version

Publishes a draft version, making it the active version for the prompt and archiving the previously published version.

### Endpoint

```
POST /v1/tenants/{tenantId}/llm/prompts/{promptId}/versions/{versionId}/publish
```

### Permission

`llm:admin`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tenantId | string | Yes | The ID of the tenant |
| promptId | string | Yes | The ID of the prompt |
| versionId | string | Yes | The ID of the version |

### Response Parameters

Returns the published prompt version object.

### Example

#### Request

```bash
curl -X POST "https://api.aisera.com/v1/tenants/9000/llm/prompts/pr_123456/versions/v_ghi789/publish" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Python Example

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com"
tenant_id = "9000"
prompt_id = "pr_123456"
version_id = "v_ghi789"

response = requests.post(
    f"{base_url}/v1/tenants/{tenant_id}/llm/prompts/{prompt_id}/versions/{version_id}/publish",
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

#### Response

```json
{
  "id": "v_ghi789",
  "promptId": "pr_123456",
  "version": 4,
  "status": "published",
  "template": "Provide an answer about {{topic}} in a {{tone}} tone. Question: {{question}}",
  "parameters": {
    "topic": {
      "type": "string",
      "description": "The topic area of the question",
      "required": true
    },
    "question": {
      "type": "string",
      "description": "The question to answer",
      "required": true
    },
    "tone": {
      "type": "string",
      "description": "The tone to use in the response",
      "enum": ["formal", "casual", "technical"],
      "default": "formal"
    }
  },
  "defaultModel": "gpt-4",
  "description": "Revised enhanced prompt with tone control",
  "createdAt": "2023-09-01T10:23:45Z",
  "createdBy": "user@example.com",
  "updatedAt": "2023-09-01T11:05:33Z",
  "updatedBy": "user@example.com",
  "publishedAt": "2023-09-01T14:20:15Z",
  "publishedBy": "admin@example.com"
}
```