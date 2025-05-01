# API Reference

## Table of Contents

- [Introduction](#introduction)
- [API Conventions](#api-conventions)
  - [Endpoint Structure](#endpoint-structure)
  - [HTTP Methods](#http-methods)
  - [Request Format](#request-format)
  - [Response Format](#response-format)
  - [Status Codes](#status-codes)
  - [Pagination](#pagination)
  - [Filtering and Sorting](#filtering-and-sorting)
  - [Error Handling](#error-handling)
- [Authentication and Authorization](#authentication-and-authorization)
  - [Authentication Methods](#authentication-methods)
  - [Authorization Scopes](#authorization-scopes)
  - [Token Management](#token-management)
- [Core API Endpoints](#core-api-endpoints)
  - [LLM Execution API](#llm-execution-api)
  - [Prompt Management API](#prompt-management-api)
  - [Provider Management API](#provider-management-api)
  - [Analytics API](#analytics-api)
  - [Health and Status API](#health-and-status-api)
- [Advanced Features](#advanced-features)
  - [Streaming Responses](#streaming-responses)
  - [Function Calling](#function-calling)
  - [Batch Processing](#batch-processing)
  - [Asynchronous Execution](#asynchronous-execution)
- [Request and Response Examples](#request-and-response-examples)
  - [LLM Execution Examples](#llm-execution-examples)
  - [Prompt Management Examples](#prompt-management-examples)
  - [Provider Management Examples](#provider-management-examples)
  - [Analytics API Examples](#analytics-api-examples)
- [Webhook API](#webhook-api)
  - [Webhook Registration](#webhook-registration)
  - [Webhook Events](#webhook-events)
  - [Webhook Payload Format](#webhook-payload-format)
- [gRPC Interface](#grpc-interface)
  - [Service Definitions](#service-definitions)
  - [Message Types](#message-types)
  - [gRPC Methods](#grpc-methods)
- [SDK References](#sdk-references)
  - [Java SDK](#java-sdk)
  - [Python SDK](#python-sdk)
  - [Node.js SDK](#nodejs-sdk)
  - [Other SDKs](#other-sdks)
- [API Versioning and Deprecation](#api-versioning-and-deprecation)
  - [Version Format](#version-format)
  - [Version Lifecycle](#version-lifecycle)
  - [Breaking vs. Non-Breaking Changes](#breaking-vs-non-breaking-changes)

## Introduction

This document provides a comprehensive reference for the LLM Gateway API, including endpoint details, authentication mechanisms, request/response formats, and example usage. The API enables applications to leverage LLM capabilities through a unified interface that simplifies integration with multiple LLM providers.

The API follows RESTful principles with additional support for streaming via Server-Sent Events (SSE) and a full gRPC interface for high-performance use cases. This reference covers both synchronous and asynchronous interaction patterns, as well as advanced features like function calling and batch processing.

## API Conventions

### Endpoint Structure

The LLM Gateway API follows a consistent URL structure:

```
https://{hostname}/api/v{version}/{resource}[/{resourceId}][/{subresource}]
```

Components of the URL structure:

- **hostname**: The domain hosting the LLM Gateway API
- **version**: API version number (e.g., `v1`)
- **resource**: Primary resource being accessed (e.g., `prompts`, `providers`)
- **resourceId**: Optional identifier for a specific resource instance
- **subresource**: Optional sub-resource related to the primary resource

**Examples:**

- `https://api.example.com/api/v1/prompts` - List all prompts
- `https://api.example.com/api/v1/prompts/123` - Get prompt with ID 123
- `https://api.example.com/api/v1/prompts/123/versions` - List versions of prompt 123

### HTTP Methods

The API uses standard HTTP methods to perform operations on resources:

| Method | Description | Idempotent | Safe |
|--------|-------------|------------|------|
| GET | Retrieve a resource or collection | Yes | Yes |
| POST | Create a new resource or execute an action | No | No |
| PUT | Replace or update a resource | Yes | No |
| PATCH | Partially update a resource | No | No |
| DELETE | Remove a resource | Yes | No |

### Request Format

API requests follow these format conventions:

- **Content-Type**: `application/json` for REST API
- **Accept**: `application/json` for synchronous responses, `text/event-stream` for streaming responses
- **Character Encoding**: UTF-8
- **Date Format**: ISO 8601 (e.g., `2023-05-15T14:22:18Z`)
- **Case Sensitivity**: Resource paths are case-sensitive

**Request Headers:**

```
Content-Type: application/json
Accept: application/json
Authorization: Bearer {token}
X-Request-ID: req-1234-5678-90ab-cdef
X-API-Key: apikey_12345
```

**Query Parameters:**

- Standard parameters are snake_case (e.g., `page_size`, `sort_by`)
- Boolean parameters accept `true` or `false`
- List parameters can be comma-separated or repeated parameters
- Filter parameters use the format `field=value` or `field[operator]=value`

### Response Format

API responses follow these format conventions:

**JSON Response Structure:**

```json
{
  "data": {
    // Main response data
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  },
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_pages": 5,
    "total_items": 42
  }
}
```

**Response Headers:**

```
Content-Type: application/json
X-Request-ID: req-1234-5678-90ab-cdef
X-Rate-Limit-Limit: 1000
X-Rate-Limit-Remaining: 995
X-Rate-Limit-Reset: 1589458800
```

### Status Codes

The API uses standard HTTP status codes to indicate the result of operations:

**Success Codes:**

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Successful request with response body |
| 201 | Created | Resource created successfully |
| 202 | Accepted | Request accepted for processing |
| 204 | No Content | Successful request with no response body |

**Client Error Codes:**

| Code | Status | Description |
|------|--------|-------------|
| 400 | Bad Request | Invalid request format or parameters |
| 401 | Unauthorized | Authentication failure |
| 403 | Forbidden | Authorization failure |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource state conflict |
| 422 | Unprocessable Entity | Semantic validation error |
| 429 | Too Many Requests | Rate limit exceeded |

**Server Error Codes:**

| Code | Status | Description |
|------|--------|-------------|
| 500 | Internal Server Error | Unexpected server error |
| 502 | Bad Gateway | Error from upstream service |
| 503 | Service Unavailable | Service temporarily unavailable |
| 504 | Gateway Timeout | Upstream service timeout |

### Pagination

The API supports pagination for list operations:

**Request Parameters:**

```
GET /api/v1/prompts?page=2&page_size=10
```

**Response Pagination Object:**

```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "page_size": 10,
    "total_pages": 5,
    "total_items": 42,
    "links": {
      "self": "/api/v1/prompts?page=2&page_size=10",
      "first": "/api/v1/prompts?page=1&page_size=10",
      "prev": "/api/v1/prompts?page=1&page_size=10",
      "next": "/api/v1/prompts?page=3&page_size=10",
      "last": "/api/v1/prompts?page=5&page_size=10"
    }
  }
}
```

**Pagination Parameters:**

- `page`: Page number (1-based)
- `page_size`: Number of items per page (default 10, max 100)
- `cursor`: Alternative cursor-based pagination token
- `limit`: Alternative to page_size

### Filtering and Sorting

The API supports filtering and sorting for list operations:

**Filtering:**

```
GET /api/v1/prompts?status=published&created_after=2023-01-01T00:00:00Z
GET /api/v1/prompts?name[contains]=assistant&tag=customer-service
```

**Sorting:**

```
GET /api/v1/prompts?sort=name
GET /api/v1/prompts?sort=-created_at,name
```

Prefix fields with `-` for descending order. Multiple sort fields are comma-separated.

### Error Handling

The API returns standardized error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request could not be processed due to validation errors",
    "details": [
      {
        "field": "prompt",
        "message": "Prompt text must not be empty",
        "constraint": "notEmpty"
      },
      {
        "field": "maxTokens",
        "message": "Maximum tokens must be between 1 and 4096",
        "constraint": "range",
        "min": 1,
        "max": 4096
      }
    ],
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z",
    "documentation": "https://docs.example.com/api/errors#validation_error"
  }
}
```

**Error Response Properties:**

- `code`: Machine-readable error code
- `message`: Human-readable error message
- `details`: Array of detailed error information
- `request_id`: Request identifier for tracing
- `timestamp`: Error timestamp
- `documentation`: Link to documentation about the error

## Authentication and Authorization

### Authentication Methods

The LLM Gateway API supports multiple authentication methods:

```mermaid
graph TD
    Client[Client Application] --> |1. Authenticate| AuthN[Authentication Layer]
    
    subgraph "Authentication Methods"
        APIKey[API Key]
        OAuth[OAuth 2.0]
        JWT[JWT]
        BasicAuth[HTTP Basic]
        MutualTLS[Mutual TLS]
    end
    
    AuthN --> APIKey
    AuthN --> OAuth
    AuthN --> JWT
    AuthN --> BasicAuth
    AuthN --> MutualTLS
    
    APIKey --> |Validate| TokenValidation[Token Validation]
    OAuth --> |Validate| TokenValidation
    JWT --> |Validate| TokenValidation
    BasicAuth --> |Validate| CredentialValidation[Credential Validation]
    MutualTLS --> |Validate| CertValidation[Certificate Validation]
    
    TokenValidation --> |Success| AuthZ[Authorization Layer]
    CredentialValidation --> |Success| AuthZ
    CertValidation --> |Success| AuthZ
    
    TokenValidation --> |Failure| AuthNFailure[Authentication Failure]
    CredentialValidation --> |Failure| AuthNFailure
    CertValidation --> |Failure| AuthNFailure
```

**1. API Key Authentication:**

```
GET /api/v1/prompts
X-API-Key: apikey_12345
```

**2. OAuth 2.0 Authentication:**

```
GET /api/v1/prompts
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**3. Basic Authentication:**

```
GET /api/v1/prompts
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**4. Mutual TLS Authentication:**

Client and server authenticate each other using X.509 certificates.

### Authorization Scopes

The API uses scopes to control access to resources:

| Scope | Description | Example Usage |
|-------|-------------|---------------|
| `llm:execute` | Execute LLM prompts | Basic prompt execution |
| `llm:execute:function` | Execute with function calling | Function calling capability |
| `prompt:read` | Read prompt templates | View existing prompts |
| `prompt:write` | Create and modify prompt templates | Manage prompts |
| `provider:read` | Read provider configurations | View provider settings |
| `provider:write` | Modify provider configurations | Manage providers |
| `analytics:read` | Access analytics data | View usage metrics |
| `admin:full` | Full administrative access | System administration |

Scopes are combined with resource-specific permissions and tenant context to determine effective permissions.

### Token Management

**Token Acquisition:**

```
POST /api/v1/auth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id=client123&client_secret=secret456&scope=llm:execute prompt:read
```

**Token Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "llm:execute prompt:read",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Token Refresh:**

```
POST /api/v1/auth/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Token Revocation:**

```
POST /api/v1/auth/revoke
Content-Type: application/x-www-form-urlencoded

token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...&token_type_hint=access_token
```

## Core API Endpoints

### LLM Execution API

The LLM Execution API enables applications to send prompts to LLM providers and receive responses.

**Endpoint Summary:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/llm/execute` | POST | Execute a prompt with an LLM provider |
| `/api/v1/llm/execute/chat` | POST | Execute a chat-based prompt |
| `/api/v1/llm/execute/stream` | POST | Execute a prompt with streaming response |
| `/api/v1/llm/execute/async` | POST | Execute a prompt asynchronously |
| `/api/v1/llm/results/{resultId}` | GET | Retrieve an asynchronous execution result |

**Basic Prompt Execution:**

```mermaid
sequenceDiagram
    participant Client
    participant Gateway as LLM Gateway
    participant LLMProvider as LLM Provider
    
    Client->>Gateway: POST /api/v1/llm/execute
    Gateway->>Gateway: Validate Request
    Gateway->>Gateway: Apply Prompt Template
    Gateway->>Gateway: Check Cache
    
    alt Cache Hit
        Gateway->>Gateway: Retrieve from Cache
    else Cache Miss
        Gateway->>LLMProvider: Forward to Provider
        LLMProvider->>Gateway: LLM Response
        Gateway->>Gateway: Process Response
        Gateway->>Gateway: Cache Response
    end
    
    Gateway->>Client: Return Response
```

**Chat-Based Execution:**

```mermaid
sequenceDiagram
    participant Client
    participant Gateway as LLM Gateway
    participant LLMProvider as LLM Provider
    
    Client->>Gateway: POST /api/v1/llm/execute/chat
    Gateway->>Gateway: Validate Request
    Gateway->>Gateway: Apply Chat Template
    Gateway->>Gateway: Check Cache
    
    alt Cache Hit
        Gateway->>Gateway: Retrieve from Cache
    else Cache Miss
        Gateway->>LLMProvider: Forward to Provider
        LLMProvider->>Gateway: LLM Response
        Gateway->>Gateway: Process Response
        Gateway->>Gateway: Cache Response
    end
    
    Gateway->>Client: Return Response
```

**Request and Response Format:**

**Prompt Execution Request:**

```json
{
  "prompt": "Explain the concept of quantum computing",
  "max_tokens": 500,
  "temperature": 0.7,
  "provider": "openai",
  "model": "gpt-4",
  "options": {
    "top_p": 0.95,
    "frequency_penalty": 0.5,
    "presence_penalty": 0.5
  },
  "cache": true
}
```

**Prompt Execution Response:**

```json
{
  "data": {
    "response": "Quantum computing is a type of computing that uses quantum-mechanical phenomena, such as superposition and entanglement, to perform operations on data...",
    "provider": "openai",
    "model": "gpt-4",
    "usage": {
      "prompt_tokens": 6,
      "completion_tokens": 128,
      "total_tokens": 134
    },
    "metadata": {
      "finish_reason": "stop",
      "cached": false
    }
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

**Chat Execution Request:**

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Explain the concept of quantum computing."
    }
  ],
  "max_tokens": 500,
  "temperature": 0.7,
  "provider": "anthropic",
  "model": "claude-2",
  "options": {
    "top_p": 0.95
  },
  "cache": true
}
```

**Chat Execution Response:**

```json
{
  "data": {
    "message": {
      "role": "assistant",
      "content": "Quantum computing is a type of computing that uses quantum-mechanical phenomena, such as superposition and entanglement, to perform operations on data..."
    },
    "provider": "anthropic",
    "model": "claude-2",
    "usage": {
      "prompt_tokens": 25,
      "completion_tokens": 128,
      "total_tokens": 153
    },
    "metadata": {
      "finish_reason": "stop",
      "cached": false
    }
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

### Prompt Management API

The Prompt Management API enables applications to create, retrieve, update, and delete prompt templates.

**Endpoint Summary:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/prompts` | GET | List all prompt templates |
| `/api/v1/prompts` | POST | Create a new prompt template |
| `/api/v1/prompts/{promptId}` | GET | Retrieve a specific prompt template |
| `/api/v1/prompts/{promptId}` | PUT | Update a prompt template |
| `/api/v1/prompts/{promptId}` | DELETE | Delete a prompt template |
| `/api/v1/prompts/{promptId}/versions` | GET | List versions of a prompt template |
| `/api/v1/prompts/{promptId}/versions/{versionId}` | GET | Get a specific version |
| `/api/v1/prompts/{promptId}/publish` | POST | Publish a draft prompt template |
| `/api/v1/prompts/{promptId}/execute` | POST | Execute a specific prompt template |

**Request and Response Format:**

**Create Prompt Template Request:**

```json
{
  "name": "Customer Support Assistant",
  "description": "Template for answering customer support questions",
  "template": "You are a helpful customer support agent.\n\nHere is information about our products: {{context}}\n\nUser question: {{question}}\n\nProvide a helpful response:",
  "parameters": [
    {
      "name": "context",
      "type": "text",
      "description": "Product information",
      "required": true
    },
    {
      "name": "question",
      "type": "text",
      "description": "User's question",
      "required": true
    }
  ],
  "provider_settings": {
    "default_provider": "openai",
    "default_model": "gpt-3.5-turbo",
    "default_parameters": {
      "temperature": 0.5,
      "max_tokens": 500
    }
  },
  "tags": ["customer-support", "product-info"]
}
```

**Create Prompt Template Response:**

```json
{
  "data": {
    "id": "pt-1234-5678-90ab-cdef",
    "name": "Customer Support Assistant",
    "description": "Template for answering customer support questions",
    "template": "You are a helpful customer support agent.\n\nHere is information about our products: {{context}}\n\nUser question: {{question}}\n\nProvide a helpful response:",
    "parameters": [
      {
        "name": "context",
        "type": "text",
        "description": "Product information",
        "required": true
      },
      {
        "name": "question",
        "type": "text",
        "description": "User's question",
        "required": true
      }
    ],
    "provider_settings": {
      "default_provider": "openai",
      "default_model": "gpt-3.5-turbo",
      "default_parameters": {
        "temperature": 0.5,
        "max_tokens": 500
      }
    },
    "tags": ["customer-support", "product-info"],
    "version": "1.0",
    "status": "draft",
    "created_by": "user-123",
    "created_at": "2023-05-15T14:22:18Z",
    "updated_at": "2023-05-15T14:22:18Z"
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

**Execute Prompt Template Request:**

```json
{
  "prompt_id": "pt-1234-5678-90ab-cdef",
  "parameters": {
    "context": "Our product XYZ is a software tool for managing customer relationships. It has features for contact management, task tracking, and email integration.",
    "question": "Does your product integrate with Gmail?"
  },
  "provider_settings": {
    "provider": "openai",
    "model": "gpt-4",
    "temperature": 0.3
  }
}
```

**Execute Prompt Template Response:**

```json
{
  "data": {
    "response": "Yes, our product XYZ integrates with Gmail. This integration allows you to sync your emails directly within the platform, track email conversations with customers, and manage your Gmail contacts within our CRM system. You can set up the integration through the Settings > Integrations menu in the application.",
    "provider": "openai",
    "model": "gpt-4",
    "usage": {
      "prompt_tokens": 84,
      "completion_tokens": 62,
      "total_tokens": 146
    },
    "metadata": {
      "prompt_id": "pt-1234-5678-90ab-cdef",
      "version": "1.0",
      "finish_reason": "stop",
      "cached": false
    }
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

### Provider Management API

The Provider Management API enables applications to manage LLM provider configurations.

**Endpoint Summary:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/providers` | GET | List all configured providers |
| `/api/v1/providers/{providerId}` | GET | Get provider configuration |
| `/api/v1/providers/{providerId}` | PUT | Update provider configuration |
| `/api/v1/providers/{providerId}/credentials` | PUT | Update provider credentials |
| `/api/v1/providers/{providerId}/models` | GET | List models for a provider |
| `/api/v1/providers/{providerId}/test` | POST | Test provider connection |

**Request and Response Format:**

**Provider Configuration:**

```json
{
  "data": {
    "id": "openai",
    "name": "OpenAI",
    "description": "OpenAI API provider",
    "status": "active",
    "endpoint": "https://api.openai.com/v1",
    "models": [
      {
        "id": "gpt-3.5-turbo",
        "name": "GPT-3.5 Turbo",
        "context_window": 4096,
        "capabilities": ["chat", "function-calling"],
        "status": "active"
      },
      {
        "id": "gpt-4",
        "name": "GPT-4",
        "context_window": 8192,
        "capabilities": ["chat", "function-calling", "vision"],
        "status": "active"
      }
    ],
    "default_model": "gpt-3.5-turbo",
    "config": {
      "timeout": 60000,
      "retry_strategy": {
        "max_retries": 3,
        "initial_backoff_ms": 1000,
        "max_backoff_ms": 10000
      },
      "rate_limits": {
        "requests_per_minute": 100,
        "tokens_per_minute": 10000
      }
    },
    "created_at": "2023-05-15T14:22:18Z",
    "updated_at": "2023-05-15T14:22:18Z"
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

**Provider Credentials Update Request:**

```json
{
  "type": "api_key",
  "credentials": {
    "api_key": "sk-1234567890abcdef"
  }
}
```

**Provider Credentials Update Response:**

```json
{
  "data": {
    "status": "active",
    "last_updated": "2023-05-15T14:22:18Z",
    "expiration": "2024-05-15T14:22:18Z"
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

### Analytics API

The Analytics API enables applications to retrieve usage and performance metrics.

**Endpoint Summary:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/analytics/usage` | GET | Get usage metrics |
| `/api/v1/analytics/usage/providers` | GET | Get usage metrics by provider |
| `/api/v1/analytics/usage/models` | GET | Get usage metrics by model |
| `/api/v1/analytics/usage/prompts` | GET | Get usage metrics by prompt template |
| `/api/v1/analytics/performance` | GET | Get performance metrics |
| `/api/v1/analytics/cost` | GET | Get cost metrics |

**Request and Response Format:**

**Usage Metrics Request:**

```
GET /api/v1/analytics/usage?start_date=2023-05-01T00:00:00Z&end_date=2023-05-15T23:59:59Z&interval=day
```

**Usage Metrics Response:**

```json
{
  "data": {
    "time_period": {
      "start": "2023-05-01T00:00:00Z",
      "end": "2023-05-15T23:59:59Z",
      "interval": "day"
    },
    "total_requests": 12583,
    "total_tokens": {
      "prompt": 1254890,
      "completion": 589305,
      "total": 1844195
    },
    "time_series": [
      {
        "date": "2023-05-01T00:00:00Z",
        "requests": 824,
        "tokens": {
          "prompt": 82341,
          "completion": 37892,
          "total": 120233
        }
      },
      {
        "date": "2023-05-02T00:00:00Z",
        "requests": 912,
        "tokens": {
          "prompt": 91205,
          "completion": 42145,
          "total": 133350
        }
      },
      // Additional days...
    ]
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-16T10:15:30Z"
  }
}
```

### Health and Status API

The Health and Status API enables applications to check the health and status of the LLM Gateway.

**Endpoint Summary:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Get system health status |
| `/api/v1/health/providers` | GET | Get provider health status |
| `/api/v1/health/components` | GET | Get component health status |
| `/api/v1/status` | GET | Get current system status |

**Request and Response Format:**

**Health Status Response:**

```json
{
  "data": {
    "status": "healthy",
    "version": "1.5.2",
    "timestamp": "2023-05-15T14:22:18Z",
    "components": {
      "api": {
        "status": "healthy",
        "latency_ms": 12
      },
      "database": {
        "status": "healthy",
        "latency_ms": 25
      },
      "cache": {
        "status": "healthy",
        "latency_ms": 3
      },
      "providers": {
        "openai": {
          "status": "healthy",
          "latency_ms": 245
        },
        "anthropic": {
          "status": "degraded",
          "latency_ms": 580,
          "message": "Elevated response times"
        },
        "bedrock": {
          "status": "healthy",
          "latency_ms": 320
        }
      }
    }
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

## Advanced Features

### Streaming Responses

The API supports streaming responses for real-time display of LLM outputs.

**Streaming Request:**

```
POST /api/v1/llm/execute/stream
Content-Type: application/json
Accept: text/event-stream

{
  "prompt": "Write a story about a space explorer",
  "max_tokens": 500,
  "temperature": 0.7,
  "provider": "openai",
  "model": "gpt-4"
}
```

**Streaming Response:**

```
event: start
data: {"request_id":"req-1234-5678-90ab-cdef","created_at":"2023-05-15T14:22:18Z"}

event: token
data: {"text":"Once","index":0}

event: token
data: {"text":" upon","index":1}

event: token
data: {"text":" a","index":2}

event: token
data: {"text":" time","index":3}

// Additional tokens...

event: metadata
data: {"usage":{"prompt_tokens":9,"completion_tokens":127,"total_tokens":136}}

event: finish
data: {"finish_reason":"stop"}
```

**Streaming Implementation:**

```mermaid
sequenceDiagram
    participant Client
    participant Gateway as LLM Gateway
    participant LLMProvider as LLM Provider
    
    Client->>Gateway: POST /api/v1/llm/execute/stream
    Gateway->>Gateway: Validate Request
    Gateway->>LLMProvider: Stream Request
    
    LLMProvider-->>Gateway: Token 1
    Gateway-->>Client: SSE: Token 1
    
    LLMProvider-->>Gateway: Token 2
    Gateway-->>Client: SSE: Token 2
    
    LLMProvider-->>Gateway: Token 3
    Gateway-->>Client: SSE: Token 3
    
    LLMProvider-->>Gateway: Completion
    Gateway-->>Client: SSE: Metadata
    Gateway-->>Client: SSE: Finish
```

### Function Calling

The API supports function calling for LLM-powered applications.

**Function Calling Request:**

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What's the weather like in San Francisco?"
    }
  ],
  "functions": [
    {
      "name": "get_weather",
      "description": "Get the current weather in a given location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA"
          },
          "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "description": "The temperature unit to use"
          }
        },
        "required": ["location"]
      }
    }
  ],
  "provider": "openai",
  "model": "gpt-4"
}
```

**Function Calling Response:**

```json
{
  "data": {
    "message": {
      "role": "assistant",
      "content": null,
      "function_call": {
        "name": "get_weather",
        "arguments": "{\"location\":\"San Francisco, CA\",\"unit\":\"celsius\"}"
      }
    },
    "provider": "openai",
    "model": "gpt-4",
    "usage": {
      "prompt_tokens": 82,
      "completion_tokens": 18,
      "total_tokens": 100
    },
    "metadata": {
      "finish_reason": "function_call",
      "cached": false
    }
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

### Batch Processing

The API supports batch processing for efficient handling of multiple requests.

**Batch Request:**

```json
{
  "requests": [
    {
      "id": "req1",
      "prompt": "Summarize the concept of machine learning",
      "max_tokens": 100,
      "provider": "openai",
      "model": "gpt-3.5-turbo"
    },
    {
      "id": "req2",
      "prompt": "Explain the difference between supervised and unsupervised learning",
      "max_tokens": 150,
      "provider": "anthropic",
      "model": "claude-2"
    },
    {
      "id": "req3",
      "prompt": "What is reinforcement learning?",
      "max_tokens": 100,
      "provider": "openai",
      "model": "gpt-4"
    }
  ],
  "execution_strategy": "parallel",
  "error_strategy": "continue"
}
```

**Batch Response:**

```json
{
  "data": {
    "results": [
      {
        "id": "req1",
        "status": "success",
        "response": {
          "response": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed...",
          "provider": "openai",
          "model": "gpt-3.5-turbo",
          "usage": {
            "prompt_tokens": 7,
            "completion_tokens": 53,
            "total_tokens": 60
          }
        }
      },
      {
        "id": "req2",
        "status": "success",
        "response": {
          "response": "Supervised learning uses labeled data for training, where the algorithm learns to map inputs to known outputs. Unsupervised learning works with unlabeled data...",
          "provider": "anthropic",
          "model": "claude-2",
          "usage": {
            "prompt_tokens": 12,
            "completion_tokens": 61,
            "total_tokens": 73
          }
        }
      },
      {
        "id": "req3",
        "status": "success",
        "response": {
          "response": "Reinforcement learning is a type of machine learning where an agent learns to make decisions by performing actions and receiving rewards or penalties...",
          "provider": "openai",
          "model": "gpt-4",
          "usage": {
            "prompt_tokens": 6,
            "completion_tokens": 48,
            "total_tokens": 54
          }
        }
      }
    ],
    "summary": {
      "total": 3,
      "succeeded": 3,
      "failed": 0,
      "total_tokens": 187
    }
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

### Asynchronous Execution

The API supports asynchronous execution for long-running operations.

**Asynchronous Request:**

```json
{
  "prompt": "Write a detailed essay on the history of artificial intelligence",
  "max_tokens": 4000,
  "temperature": 0.7,
  "provider": "openai",
  "model": "gpt-4",
  "callback_url": "https://example.com/api/callbacks"
}
```

**Asynchronous Response (Immediate):**

```json
{
  "data": {
    "request_id": "req-1234-5678-90ab-cdef",
    "status": "processing",
    "result_url": "/api/v1/llm/results/res-1234-5678-90ab-cdef",
    "estimated_completion_time": "2023-05-15T14:23:18Z"
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

**Check Result Request:**

```
GET /api/v1/llm/results/res-1234-5678-90ab-cdef
```

**Check Result Response:**

```json
{
  "data": {
    "request_id": "req-1234-5678-90ab-cdef",
    "status": "completed",
    "result": {
      "response": "The history of artificial intelligence begins in antiquity with myths, stories and rumors of artificial beings endowed with intelligence...",
      "provider": "openai",
      "model": "gpt-4",
      "usage": {
        "prompt_tokens": 11,
        "completion_tokens": 1523,
        "total_tokens": 1534
      },
      "metadata": {
        "finish_reason": "stop",
        "cached": false
      }
    },
    "created_at": "2023-05-15T14:22:18Z",
    "completed_at": "2023-05-15T14:23:15Z"
  },
  "meta": {
    "request_id": "req-5678-1234-cdef-90ab",
    "timestamp": "2023-05-15T14:23:20Z"
  }
}
```

**Callback Payload:**

```json
{
  "event_type": "llm.execution.completed",
  "resource_type": "llm_execution",
  "resource_id": "res-1234-5678-90ab-cdef",
  "timestamp": "2023-05-15T14:23:15Z",
  "data": {
    "request_id": "req-1234-5678-90ab-cdef",
    "status": "completed",
    "result": {
      "response": "The history of artificial intelligence begins in antiquity with myths, stories and rumors of artificial beings endowed with intelligence...",
      "provider": "openai",
      "model": "gpt-4",
      "usage": {
        "prompt_tokens": 11,
        "completion_tokens": 1523,
        "total_tokens": 1534
      },
      "metadata": {
        "finish_reason": "stop",
        "cached": false
      }
    }
  }
}
```

## Request and Response Examples

### LLM Execution Examples

**Example 1: Basic Text Completion**

```json
// Request
POST /api/v1/llm/execute
{
  "prompt": "Explain the concept of machine learning in simple terms",
  "max_tokens": 200,
  "temperature": 0.7,
  "provider": "openai",
  "model": "gpt-3.5-turbo"
}

// Response
{
  "data": {
    "response": "Machine learning is like teaching a computer to learn from examples, much like how a child learns from experience. Instead of programming specific instructions for every possible situation, we show the computer lots of examples and it figures out patterns on its own...",
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "usage": {
      "prompt_tokens": 11,
      "completion_tokens": 85,
      "total_tokens": 96
    },
    "metadata": {
      "finish_reason": "length",
      "cached": false
    }
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

**Example 2: Chat Completion**

```json
// Request
POST /api/v1/llm/execute/chat
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant that specializes in technology explanations."
    },
    {
      "role": "user",
      "content": "What is the difference between REST and GraphQL?"
    }
  ],
  "max_tokens": 300,
  "temperature": 0.5,
  "provider": "anthropic",
  "model": "claude-2"
}

// Response
{
  "data": {
    "message": {
      "role": "assistant",
      "content": "REST and GraphQL are both approaches for building APIs, but they have different philosophies and capabilities:\n\n**REST (Representational State Transfer)**:\n- Uses standard HTTP methods (GET, POST, PUT, DELETE)\n- Operates on resources with fixed endpoints for each resource type\n- Returns fixed data structures defined by the server\n- Typically requires multiple requests to fetch related data\n- Simple caching with HTTP cache headers\n\n**GraphQL**:\n- Uses a single endpoint for all operations\n- Clients specify exactly what data they need in the query\n- Returns precisely the data requested, no more or less\n- Can fetch multiple related resources in a single request\n- Requires custom caching solutions\n- Provides introspection to explore the API schema\n\nIn essence, REST is simpler but less flexible, while GraphQL gives clients more control over exactly what data they receive but with added complexity in implementation."
    },
    "provider": "anthropic",
    "model": "claude-2",
    "usage": {
      "prompt_tokens": 34,
      "completion_tokens": 205,
      "total_tokens": 239
    },
    "metadata": {
      "finish_reason": "stop",
      "cached": false
    }
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

### Prompt Management Examples

**Example 1: Create a Prompt Template**

```json
// Request
POST /api/v1/prompts
{
  "name": "SQL Query Generator",
  "description": "Generate SQL queries based on natural language descriptions",
  "template": "You are an expert SQL developer. Your task is to generate a SQL query based on the following requirements:\n\nDatabase schema:\n{{schema}}\n\nQuery request: {{request}}\n\nGenerate ONLY the SQL query without any explanations:",
  "parameters": [
    {
      "name": "schema",
      "type": "text",
      "description": "Database schema description",
      "required": true
    },
    {
      "name": "request",
      "type": "text",
      "description": "Natural language description of the desired query",
      "required": true
    }
  ],
  "provider_settings": {
    "default_provider": "openai",
    "default_model": "gpt-4",
    "default_parameters": {
      "temperature": 0.2,
      "max_tokens": 300
    }
  },
  "tags": ["sql", "database", "code-generation"]
}

// Response
{
  "data": {
    "id": "pt-1234-5678-90ab-cdef",
    "name": "SQL Query Generator",
    "description": "Generate SQL queries based on natural language descriptions",
    "template": "You are an expert SQL developer. Your task is to generate a SQL query based on the following requirements:\n\nDatabase schema:\n{{schema}}\n\nQuery request: {{request}}\n\nGenerate ONLY the SQL query without any explanations:",
    "parameters": [
      {
        "name": "schema",
        "type": "text",
        "description": "Database schema description",
        "required": true
      },
      {
        "name": "request",
        "type": "text",
        "description": "Natural language description of the desired query",
        "required": true
      }
    ],
    "provider_settings": {
      "default_provider": "openai",
      "default_model": "gpt-4",
      "default_parameters": {
        "temperature": 0.2,
        "max_tokens": 300
      }
    },
    "tags": ["sql", "database", "code-generation"],
    "version": "1.0",
    "status": "draft",
    "created_by": "user-123",
    "created_at": "2023-05-15T14:22:18Z",
    "updated_at": "2023-05-15T14:22:18Z"
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

**Example 2: Execute a Prompt Template**

```json
// Request
POST /api/v1/prompts/pt-1234-5678-90ab-cdef/execute
{
  "parameters": {
    "schema": "Tables:\n- users(id, name, email, created_at)\n- orders(id, user_id, total, status, created_at)\n- order_items(id, order_id, product_id, quantity, price)",
    "request": "Find all users who have placed orders with a total value greater than $100 in the last 30 days"
  }
}

// Response
{
  "data": {
    "response": "SELECT DISTINCT u.id, u.name, u.email\nFROM users u\nJOIN orders o ON u.id = o.user_id\nWHERE o.total > 100\nAND o.created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)\nAND o.status = 'completed'\nORDER BY u.name;",
    "provider": "openai",
    "model": "gpt-4",
    "usage": {
      "prompt_tokens": 128,
      "completion_tokens": 42,
      "total_tokens": 170
    },
    "metadata": {
      "prompt_id": "pt-1234-5678-90ab-cdef",
      "version": "1.0",
      "finish_reason": "stop",
      "cached": false
    }
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

### Provider Management Examples

**Example 1: List Providers**

```json
// Request
GET /api/v1/providers

// Response
{
  "data": [
    {
      "id": "openai",
      "name": "OpenAI",
      "description": "OpenAI API provider",
      "status": "active",
      "default_model": "gpt-3.5-turbo",
      "models_count": 5,
      "created_at": "2023-05-15T14:22:18Z",
      "updated_at": "2023-05-15T14:22:18Z"
    },
    {
      "id": "anthropic",
      "name": "Anthropic",
      "description": "Anthropic API provider",
      "status": "active",
      "default_model": "claude-2",
      "models_count": 3,
      "created_at": "2023-05-15T14:22:18Z",
      "updated_at": "2023-05-15T14:22:18Z"
    },
    {
      "id": "bedrock",
      "name": "AWS Bedrock",
      "description": "AWS Bedrock API provider",
      "status": "active",
      "default_model": "amazon.titan-tg1-large",
      "models_count": 8,
      "created_at": "2023-05-15T14:22:18Z",
      "updated_at": "2023-05-15T14:22:18Z"
    }
  ],
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

**Example 2: Update Provider Configuration**

```json
// Request
PUT /api/v1/providers/openai
{
  "status": "active",
  "endpoint": "https://api.openai.com/v1",
  "default_model": "gpt-4",
  "config": {
    "timeout": 90000,
    "retry_strategy": {
      "max_retries": 5,
      "initial_backoff_ms": 1000,
      "max_backoff_ms": 20000
    },
    "rate_limits": {
      "requests_per_minute": 150,
      "tokens_per_minute": 15000
    }
  }
}

// Response
{
  "data": {
    "id": "openai",
    "name": "OpenAI",
    "description": "OpenAI API provider",
    "status": "active",
    "endpoint": "https://api.openai.com/v1",
    "default_model": "gpt-4",
    "config": {
      "timeout": 90000,
      "retry_strategy": {
        "max_retries": 5,
        "initial_backoff_ms": 1000,
        "max_backoff_ms": 20000
      },
      "rate_limits": {
        "requests_per_minute": 150,
        "tokens_per_minute": 15000
      }
    },
    "created_at": "2023-05-15T14:22:18Z",
    "updated_at": "2023-05-15T14:25:30Z"
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:25:30Z"
  }
}
```

### Analytics API Examples

**Example 1: Usage by Provider**

```json
// Request
GET /api/v1/analytics/usage/providers?start_date=2023-05-01T00:00:00Z&end_date=2023-05-15T23:59:59Z

// Response
{
  "data": {
    "time_period": {
      "start": "2023-05-01T00:00:00Z",
      "end": "2023-05-15T23:59:59Z"
    },
    "total_requests": 12583,
    "providers": [
      {
        "provider": "openai",
        "requests": 8754,
        "percentage": 69.57,
        "tokens": {
          "prompt": 875490,
          "completion": 412305,
          "total": 1287795
        },
        "models": [
          {
            "model": "gpt-4",
            "requests": 3241,
            "tokens": {
              "prompt": 324190,
              "completion": 152345,
              "total": 476535
            }
          },
          {
            "model": "gpt-3.5-turbo",
            "requests": 5513,
            "tokens": {
              "prompt": 551300,
              "completion": 259960,
              "total": 811260
            }
          }
        ]
      },
      {
        "provider": "anthropic",
        "requests": 2987,
        "percentage": 23.74,
        "tokens": {
          "prompt": 298720,
          "completion": 140389,
          "total": 439109
        },
        "models": [
          {
            "model": "claude-2",
            "requests": 2987,
            "tokens": {
              "prompt": 298720,
              "completion": 140389,
              "total": 439109
            }
          }
        ]
      },
      {
        "provider": "bedrock",
        "requests": 842,
        "percentage": 6.69,
        "tokens": {
          "prompt": 80680,
          "completion": 36611,
          "total": 117291
        },
        "models": [
          {
            "model": "amazon.titan-tg1-large",
            "requests": 842,
            "tokens": {
              "prompt": 80680,
              "completion": 36611,
              "total": 117291
            }
          }
        ]
      }
    ]
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-16T10:15:30Z"
  }
}
```

## Webhook API

### Webhook Registration

```json
// Request
POST /api/v1/webhooks
{
  "url": "https://example.com/webhook/llm-gateway",
  "description": "Production environment webhook",
  "events": [
    "llm.execution.completed",
    "prompt.published",
    "provider.status_changed"
  ],
  "secret": "whsec_8UvKRPmrnXJTJNh3MrXNtyHowKBZuxtb",
  "status": "active"
}

// Response
{
  "data": {
    "id": "wh-1234-5678-90ab-cdef",
    "url": "https://example.com/webhook/llm-gateway",
    "description": "Production environment webhook",
    "events": [
      "llm.execution.completed",
      "prompt.published",
      "provider.status_changed"
    ],
    "status": "active",
    "created_at": "2023-05-15T14:22:18Z",
    "updated_at": "2023-05-15T14:22:18Z"
  },
  "meta": {
    "request_id": "req-1234-5678-90ab-cdef",
    "timestamp": "2023-05-15T14:22:18Z"
  }
}
```

### Webhook Events

| Event Type | Description | Payload Example |
|------------|-------------|-----------------|
| `llm.execution.completed` | An LLM execution has completed | Execution result data |
| `llm.execution.failed` | An LLM execution has failed | Error details |
| `prompt.created` | A new prompt template has been created | Prompt template data |
| `prompt.updated` | A prompt template has been updated | Updated prompt template data |
| `prompt.published` | A prompt template has been published | Published prompt template data |
| `prompt.deleted` | A prompt template has been deleted | Deleted prompt ID |
| `provider.status_changed` | A provider's status has changed | Provider status data |
| `provider.config_changed` | A provider's configuration has changed | Provider config data |

### Webhook Payload Format

```json
{
  "id": "evt-1234-5678-90ab-cdef",
  "event_type": "llm.execution.completed",
  "resource_type": "llm_execution",
  "resource_id": "res-1234-5678-90ab-cdef",
  "timestamp": "2023-05-15T14:23:15Z",
  "data": {
    "request_id": "req-1234-5678-90ab-cdef",
    "status": "completed",
    "result": {
      "response": "The history of artificial intelligence begins...",
      "provider": "openai",
      "model": "gpt-4",
      "usage": {
        "prompt_tokens": 11,
        "completion_tokens": 1523,
        "total_tokens": 1534
      },
      "metadata": {
        "finish_reason": "stop",
        "cached": false
      }
    }
  },
  "signature": "t=1684159395,v1=abcdefghijklmnopqrstuvwxyz1234567890"
}
```

## gRPC Interface

### Service Definitions

```protobuf
syntax = "proto3";

package com.aisera.service.llm.grpc;

service LLMService {
  // Execute a prompt with an LLM provider
  rpc ExecutePrompt(ExecutePromptRequest) returns (ExecutePromptResponse);
  
  // Execute a chat-based prompt
  rpc ExecuteChat(ExecuteChatRequest) returns (ExecuteChatResponse);
  
  // Execute a prompt with streaming response
  rpc StreamPrompt(ExecutePromptRequest) returns (stream StreamPromptResponse);
  
  // Execute a chat-based prompt with streaming response
  rpc StreamChat(ExecuteChatRequest) returns (stream StreamChatResponse);
}

service PromptService {
  // List prompt templates
  rpc ListPrompts(ListPromptsRequest) returns (ListPromptsResponse);
  
  // Get a prompt template
  rpc GetPrompt(GetPromptRequest) returns (GetPromptResponse);
  
  // Create a prompt template
  rpc CreatePrompt(CreatePromptRequest) returns (CreatePromptResponse);
  
  // Update a prompt template
  rpc UpdatePrompt(UpdatePromptRequest) returns (UpdatePromptResponse);
  
  // Delete a prompt template
  rpc DeletePrompt(DeletePromptRequest) returns (DeletePromptResponse);
  
  // Execute a prompt template
  rpc ExecutePromptTemplate(ExecutePromptTemplateRequest) returns (ExecutePromptTemplateResponse);
}
```

### Message Types

```protobuf
message ExecutePromptRequest {
  string prompt = 1;
  int32 max_tokens = 2;
  float temperature = 3;
  string provider = 4;
  string model = 5;
  map<string, string> options = 6;
  bool cache = 7;
}

message ExecutePromptResponse {
  string response = 1;
  string provider = 2;
  string model = 3;
  UsageMetrics usage = 4;
  ResponseMetadata metadata = 5;
}

message ExecuteChatRequest {
  repeated ChatMessage messages = 1;
  int32 max_tokens = 2;
  float temperature = 3;
  string provider = 4;
  string model = 5;
  map<string, string> options = 6;
  bool cache = 7;
  repeated FunctionDefinition functions = 8;
}

message ExecuteChatResponse {
  ChatMessage message = 1;
  string provider = 2;
  string model = 3;
  UsageMetrics usage = 4;
  ResponseMetadata metadata = 5;
}

message ChatMessage {
  string role = 1;
  string content = 2;
  FunctionCall function_call = 3;
}

message FunctionDefinition {
  string name = 1;
  string description = 2;
  string parameters_json = 3;
}

message FunctionCall {
  string name = 1;
  string arguments = 2;
}

message StreamPromptResponse {
  oneof event {
    StreamStart start = 1;
    StreamToken token = 2;
    StreamMetadata metadata = 3;
    StreamFinish finish = 4;
  }
}

message StreamStart {
  string request_id = 1;
  string created_at = 2;
}

message StreamToken {
  string text = 1;
  int32 index = 2;
}

message StreamMetadata {
  UsageMetrics usage = 1;
}

message StreamFinish {
  string finish_reason = 1;
}

message UsageMetrics {
  int32 prompt_tokens = 1;
  int32 completion_tokens = 2;
  int32 total_tokens = 3;
}

message ResponseMetadata {
  string finish_reason = 1;
  bool cached = 2;
  string request_id = 3;
}
```

### gRPC Methods

```mermaid
sequenceDiagram
    participant Client
    participant Service as gRPC Service
    participant Backend as LLM Gateway Backend
    
    Client->>Service: ExecutePrompt(prompt, options)
    Service->>Backend: Process Request
    Backend->>Service: Return Result
    Service->>Client: ExecutePromptResponse
    
    Client->>Service: StreamChat(messages, options)
    Service->>Backend: Process Request
    
    loop For each token
        Backend->>Service: Generate Token
        Service->>Client: StreamChatResponse with token
    end
    
    Backend->>Service: Completion
    Service->>Client: StreamChatResponse with metadata
    Service->>Client: StreamChatResponse with finish
```

## SDK References

### Java SDK

```java
// Basic usage example
import com.aisera.llm.gateway.client.LLMGatewayClient;
import com.aisera.llm.gateway.model.ExecutePromptRequest;
import com.aisera.llm.gateway.model.ExecutePromptResponse;

LLMGatewayClient client = LLMGatewayClient.builder()
    .apiKey("your-api-key")
    .endpoint("https://api.example.com")
    .build();

ExecutePromptRequest request = ExecutePromptRequest.builder()
    .prompt("Explain quantum computing in simple terms")
    .maxTokens(200)
    .temperature(0.7f)
    .provider("openai")
    .model("gpt-4")
    .build();

ExecutePromptResponse response = client.executePrompt(request);
System.out.println(response.getResponse());
```

### Python SDK

```python
# Basic usage example
from llm_gateway import LLMGatewayClient

client = LLMGatewayClient(
    api_key="your-api-key",
    endpoint="https://api.example.com"
)

response = client.execute_prompt(
    prompt="Explain quantum computing in simple terms",
    max_tokens=200,
    temperature=0.7,
    provider="openai",
    model="gpt-4"
)

print(response.text)
```

### Node.js SDK

```javascript
// Basic usage example
const { LLMGatewayClient } = require('llm-gateway');

const client = new LLMGatewayClient({
  apiKey: 'your-api-key',
  endpoint: 'https://api.example.com'
});

async function getResponse() {
  const response = await client.executePrompt({
    prompt: 'Explain quantum computing in simple terms',
    maxTokens: 200,
    temperature: 0.7,
    provider: 'openai',
    model: 'gpt-4'
  });
  
  console.log(response.text);
}

getResponse();
```

### Other SDKs

The LLM Gateway provides additional SDKs for the following languages:

- Go
- .NET (C#)
- Ruby
- PHP
- Rust

## API Versioning and Deprecation

### Version Format

The LLM Gateway API uses a simple major version format in the URL path:

```
https://api.example.com/api/v1/...
```

Major versions (e.g., v1, v2) are used for breaking changes. Non-breaking changes are made within a major version.

### Version Lifecycle

| Stage | Description | Support Timeframe |
|-------|-------------|-------------------|
| Preview | Early access, subject to change | No SLA, no stability guarantees |
| General Availability | Stable API version | Minimum 12 months |
| Deprecated | Still functional but not recommended | Minimum 6 months after deprecation notice |
| Sunset | No longer available | N/A |

### Breaking vs. Non-Breaking Changes

**Non-Breaking Changes (Within Version):**
- Adding new API endpoints
- Adding optional request parameters
- Adding response fields
- Bug fixes that don't change behavior

**Breaking Changes (New Version):**
- Removing or renaming API endpoints
- Removing or renaming required request parameters
- Changing response structure
- Changing authentication requirements

---

**Previous**: [Error Handling and Resilience](./error-handling-resilience.md) | **Back to [README](./README.md)**