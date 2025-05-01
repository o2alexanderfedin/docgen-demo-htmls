# API Reference

This section provides detailed documentation of all LLM Gateway API endpoints. Each endpoint includes information about the request parameters, response format, and example code snippets.

## API Overview

The LLM Gateway API is divided into several functional areas:

| Area | Description |
|------|-------------|
| [Prompt Management](./prompt-management.md) | Create, read, update, and delete prompts |
| [Prompt Execution](./prompt-execution.md) | Execute prompts against LLMs |
| [LLM Registry](./llm-registry.md) | Manage LLM provider registrations |
| [Versioning](./versioning.md) | Manage prompt versions |

## Base URLs

The LLM Gateway API is accessible at the following base URLs:

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.aisera.com/llm/v1` |
| Staging | `https://api-staging.aisera.com/llm/v1` |
| Development | `https://api-dev.aisera.com/llm/v1` |

## Request Format

All API requests should include the following headers:

- `Content-Type: application/json` for requests with a JSON body
- `Authorization: Bearer YOUR_TOKEN` or `X-API-Key: YOUR_API_KEY` for authentication

## Response Format

All API responses follow a standard format:

- Successful responses have a 2xx status code and return JSON
- Error responses have a non-2xx status code and return a JSON error object

### Success Response Format

```json
{
  "statusCode": 200,
  "data": {
    // Response data varies by endpoint
  }
}
```

### Error Response Format

```json
{
  "statusCode": 400,
  "errorMessage": "Descriptive error message",
  "errorCode": "ERROR_CODE"
}
```

## Endpoints by Area

### Prompt Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/prompt_group/list` | List all prompt groups |
| POST | `/prompt_group` | Create a new prompt group |
| GET | `/prompt_group` | Get a specific prompt group |
| PUT | `/prompt_group` | Update a prompt group |
| DELETE | `/prompt_group` | Delete a prompt group |
| GET | `/prompt/list` | List all prompts |
| GET | `/v1/tenants/{tenantId}/llm/prompts` | List prompts for a tenant |
| GET | `/v1/tenants/{tenantId}/llm/prompts/{promptId}` | Get a specific prompt |
| POST | `/v1/tenants/{tenantId}/llm/prompts` | Create a new prompt |
| PUT | `/v1/tenants/{tenantId}/llm/prompts/{promptId}` | Update a prompt |
| DELETE | `/v1/tenants/{tenantId}/llm/prompts/{promptId}` | Delete a prompt |

### Prompt Execution

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/execution/fetchChatAnswer` | Execute a chat-style prompt and get an answer |
| POST | `/execution/fetchAnswer` | Execute a prompt and get an answer |
| POST | `/execution/inferPrompt` | Get prompt details for execution |
| POST | `/v1/tenants/{tenantId}/llm/prompts/execute` | Execute a prompt directly |

### LLM Registry

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/tenants/{tenantId}/llm/prompts/models` | List available LLM models |
| GET | `/v1/tenants/{tenantId}/llm/prompts/providers` | List available LLM providers |

### Versioning

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/tenants/{tenantId}/version/llm-prompts` | Create a new prompt version |
| PUT | `/v1/tenants/{tenantId}/version/llm-prompts/{promptId}` | Update a prompt version |
| POST | `/v1/tenants/{tenantId}/version/llm-prompts/new-draft` | Create a new draft version |
| POST | `/v1/tenants/{tenantId}/version/llm-prompts/publish` | Publish a draft version |
| DELETE | `/v1/tenants/{tenantId}/version/llm-prompts/{promptId}` | Delete a prompt version |
| GET | `/v1/tenants/{tenantId}/version/llm-prompts/unique` | List unique prompts |
| GET | `/v1/tenants/{tenantId}/version/llm-prompts/published` | List published prompts |

## Using This Reference

Each section contains detailed information about the endpoints in that area. For each endpoint, you'll find:

- URL and HTTP method
- Required permissions
- Request parameters
- Response format
- Example requests and responses in multiple languages
- Error handling information

Navigate to the specific area to find detailed information about the endpoints you need.