# LLM Gateway API Reference

This document provides detailed information about the API endpoints exposed by the LLM Gateway.

- [REST API](#rest-api)
  - [Prompt Execution](#prompt-execution)
  - [Prompt Management](#prompt-management)
  - [LLM Registry Management](#llm-registry-management)
- [gRPC API](#grpc-api)
  - [Service Definition](#service-definition)
  - [Message Types](#message-types)
- [Common Data Structures](#common-data-structures)
- [Error Handling](#error-handling)

## REST API

The LLM Gateway exposes RESTful APIs for executing prompts and managing the prompt registry. All API requests and responses use JSON format.

Base URL: `/api/v1`

### Prompt Execution

#### Execute Prompt (Fetch)

Executes a prompt and returns a response from an LLM.

- **URL**: `/prompt/fetch`
- **Method**: `POST`
- **Auth Required**: Yes

**Request Body:**

```json
{
  "tenantId": "string",
  "promptName": "string",
  "requestParams": [
    {
      "name": "string",
      "value": "any"
    }
  ],
  "config": {
    "property1": "any",
    "property2": "any"
  },
  "isDebug": false,
  "botId": 0,
  "useCache": false,
  "detectPromptInjection": false
}
```

**Response:**

```json
{
  "statusCode": 200,
  "errorMessage": "string",
  "responseParams": [
    {
      "name": "string",
      "value": "any"
    }
  ],
  "llmDebugInfos": [
    {
      "tenantId": "string",
      "promptGroupName": "string",
      "promptName": "string",
      "appliedTemplate": "string",
      "requestParams": [
        {
          "name": "string",
          "value": "any"
        }
      ],
      "responseParams": [
        {
          "name": "string",
          "value": "any"
        }
      ],
      "responseMessage": "string",
      "timeCostInMillis": 0,
      "config": {
        "property1": "any",
        "property2": "any"
      },
      "messages": [
        {
          "role": "string",
          "content": "string",
          "contentType": "TEXT",
          "functionCall": {
            "name": "string",
            "arguments": "string"
          }
        }
      ]
    }
  ]
}
```

**Status Codes:**

- `200 OK`: Request successful
- `400 Bad Request`: Invalid input parameters
- `404 Not Found`: Prompt not found
- `500 Internal Server Error`: Server-side error

#### Execute Chat Prompt (FetchChat)

Executes a chat-style prompt and returns a response from an LLM.

- **URL**: `/prompt/fetchChat`
- **Method**: `POST`
- **Auth Required**: Yes

**Request Body:**

```json
{
  "tenantId": "string",
  "promptName": "string",
  "requestParams": [
    {
      "name": "string",
      "value": "any"
    }
  ],
  "messages": [
    {
      "role": "string",
      "content": "string",
      "contentType": "TEXT",
      "function_call": {
        "name": "string",
        "arguments": "string"
      }
    }
  ],
  "config": {
    "property1": "any",
    "property2": "any"
  },
  "isDebug": false,
  "botId": 0,
  "functionDefinitions": [
    {
      "name": "string",
      "description": "string",
      "parameters": {
        "type": "object",
        "properties": {
          "property1": {
            "type": "string",
            "description": "string"
          }
        },
        "required": [
          "string"
        ]
      }
    }
  ],
  "useCache": false,
  "detectPromptInjection": false
}
```

**Response:**

```json
{
  "statusCode": 200,
  "errorMessage": "string",
  "errorCode": "string",
  "message": "string",
  "responseParams": [
    {
      "name": "string",
      "value": "any"
    }
  ],
  "llmDebugInfos": [
    {
      "tenantId": "string",
      "promptGroupName": "string",
      "promptName": "string",
      "appliedTemplate": "string",
      "requestParams": [
        {
          "name": "string",
          "value": "any"
        }
      ],
      "responseParams": [
        {
          "name": "string",
          "value": "any"
        }
      ],
      "responseMessage": "string",
      "timeCostInMillis": 0,
      "config": {
        "property1": "any",
        "property2": "any"
      },
      "messages": [
        {
          "role": "string",
          "content": "string",
          "contentType": "TEXT",
          "functionCall": {
            "name": "string",
            "arguments": "string"
          }
        }
      ]
    }
  ]
}
```

**Status Codes:**

- `200 OK`: Request successful
- `400 Bad Request`: Invalid input parameters
- `404 Not Found`: Prompt not found
- `500 Internal Server Error`: Server-side error

#### Stream Chat Response

Streams a response from an LLM using Server-Sent Events (SSE).

- **URL**: `/prompt/stream`
- **Method**: `POST`
- **Auth Required**: Yes

**Request Body:**

```json
{
  "tenantId": "string",
  "promptName": "string",
  "requestParams": [
    {
      "name": "string",
      "value": "any"
    }
  ],
  "messages": [
    {
      "role": "string",
      "content": "string",
      "contentType": "TEXT",
      "function_call": {
        "name": "string",
        "arguments": "string"
      }
    }
  ],
  "config": {
    "property1": "any",
    "property2": "any"
  },
  "botId": 0
}
```

**Response:**

Server-Sent Events stream with response chunks.

**Status Codes:**

- `200 OK`: Stream started successfully
- `400 Bad Request`: Invalid input parameters
- `404 Not Found`: Prompt not found
- `500 Internal Server Error`: Server-side error

### Prompt Management

#### Get Prompt

Retrieves a prompt by name.

- **URL**: `/prompt/{promptName}`
- **Method**: `GET`
- **Auth Required**: Yes

**Query Parameters:**

- `tenantId` (string, required): ID of the tenant
- `botId` (number, optional): ID of the bot

**Response:**

```json
{
  "id": 0,
  "name": "string",
  "displayName": "string",
  "inputParams": [
    {
      "name": "string",
      "type": "string",
      "description": "string",
      "required": true,
      "defaultValue": "string",
      "options": [
        "string"
      ]
    }
  ],
  "template": "string",
  "userTemplate": "string",
  "outputParams": [
    {
      "name": "string",
      "type": "string",
      "description": "string",
      "required": true,
      "defaultValue": "string",
      "options": [
        "string"
      ]
    }
  ],
  "llmRegistryId": 0,
  "botId": 0,
  "status": "Active",
  "type": "string",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z",
  "isRegistered": false,
  "isImported": false,
  "isDefault": false,
  "isSystem": false,
  "category": "string",
  "useCase": "string",
  "script": "string",
  "description": "string",
  "config": {
    "property1": "any",
    "property2": "any"
  },
  "reviewStatus": "string",
  "entityGuid": "string",
  "changeLogId": 0,
  "createdBy": 0,
  "updatedBy": 0,
  "source": "string"
}
```

**Status Codes:**

- `200 OK`: Request successful
- `404 Not Found`: Prompt not found

#### Create Prompt

Creates a new prompt.

- **URL**: `/prompt`
- **Method**: `POST`
- **Auth Required**: Yes

**Request Body:**

```json
{
  "name": "string",
  "displayName": "string",
  "inputParams": [
    {
      "name": "string",
      "type": "string",
      "description": "string",
      "required": true,
      "defaultValue": "string",
      "options": [
        "string"
      ]
    }
  ],
  "template": "string",
  "userTemplate": "string",
  "outputParams": [
    {
      "name": "string",
      "type": "string",
      "description": "string",
      "required": true,
      "defaultValue": "string",
      "options": [
        "string"
      ]
    }
  ],
  "llmRegistryId": 0,
  "botId": 0,
  "type": "string",
  "category": "string",
  "useCase": "string",
  "script": "string",
  "description": "string",
  "config": {
    "property1": "any",
    "property2": "any"
  }
}
```

**Response:**

```json
{
  "id": 0,
  "name": "string",
  "displayName": "string",
  "inputParams": [
    {
      "name": "string",
      "type": "string",
      "description": "string",
      "required": true,
      "defaultValue": "string",
      "options": [
        "string"
      ]
    }
  ],
  "template": "string",
  "userTemplate": "string",
  "outputParams": [
    {
      "name": "string",
      "type": "string",
      "description": "string",
      "required": true,
      "defaultValue": "string",
      "options": [
        "string"
      ]
    }
  ],
  "llmRegistryId": 0,
  "botId": 0,
  "status": "Active",
  "type": "string",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z",
  "isRegistered": false,
  "isImported": false,
  "isDefault": false,
  "isSystem": false,
  "category": "string",
  "useCase": "string",
  "script": "string",
  "description": "string",
  "config": {
    "property1": "any",
    "property2": "any"
  },
  "reviewStatus": "string",
  "entityGuid": "string",
  "changeLogId": 0,
  "createdBy": 0,
  "updatedBy": 0,
  "source": "string"
}
```

**Status Codes:**

- `201 Created`: Prompt created successfully
- `400 Bad Request`: Invalid input parameters
- `409 Conflict`: Prompt with the same name already exists

#### Update Prompt

Updates an existing prompt.

- **URL**: `/prompt/{promptName}`
- **Method**: `PUT`
- **Auth Required**: Yes

**Query Parameters:**

- `tenantId` (string, required): ID of the tenant
- `botId` (number, optional): ID of the bot

**Request Body:**

```json
{
  "displayName": "string",
  "inputParams": [
    {
      "name": "string",
      "type": "string",
      "description": "string",
      "required": true,
      "defaultValue": "string",
      "options": [
        "string"
      ]
    }
  ],
  "template": "string",
  "userTemplate": "string",
  "outputParams": [
    {
      "name": "string",
      "type": "string",
      "description": "string",
      "required": true,
      "defaultValue": "string",
      "options": [
        "string"
      ]
    }
  ],
  "llmRegistryId": 0,
  "type": "string",
  "category": "string",
  "useCase": "string",
  "script": "string",
  "description": "string",
  "config": {
    "property1": "any",
    "property2": "any"
  }
}
```

**Response:**

```json
{
  "id": 0,
  "name": "string",
  "displayName": "string",
  "inputParams": [
    {
      "name": "string",
      "type": "string",
      "description": "string",
      "required": true,
      "defaultValue": "string",
      "options": [
        "string"
      ]
    }
  ],
  "template": "string",
  "userTemplate": "string",
  "outputParams": [
    {
      "name": "string",
      "type": "string",
      "description": "string",
      "required": true,
      "defaultValue": "string",
      "options": [
        "string"
      ]
    }
  ],
  "llmRegistryId": 0,
  "botId": 0,
  "status": "Active",
  "type": "string",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z",
  "isRegistered": false,
  "isImported": false,
  "isDefault": false,
  "isSystem": false,
  "category": "string",
  "useCase": "string",
  "script": "string",
  "description": "string",
  "config": {
    "property1": "any",
    "property2": "any"
  },
  "reviewStatus": "string",
  "entityGuid": "string",
  "changeLogId": 0,
  "createdBy": 0,
  "updatedBy": 0,
  "source": "string"
}
```

**Status Codes:**

- `200 OK`: Prompt updated successfully
- `400 Bad Request`: Invalid input parameters
- `404 Not Found`: Prompt not found

### LLM Registry Management

#### Get LLM Registry Entry

Retrieves an LLM registry entry by name.

- **URL**: `/llm/{llmName}`
- **Method**: `GET`
- **Auth Required**: Yes

**Response:**

```json
{
  "id": 0,
  "name": "string",
  "displayName": "string",
  "description": "string",
  "category": "string",
  "isActive": true,
  "endpoint": "string",
  "config": {
    "property1": "any",
    "property2": "any"
  },
  "authConfig": {
    "property1": "any",
    "property2": "any"
  },
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z"
}
```

**Status Codes:**

- `200 OK`: Request successful
- `404 Not Found`: LLM registry entry not found

## gRPC API

The LLM Gateway also exposes a gRPC API for efficient binary communication.

### Service Definition

```protobuf
syntax = "proto3";

package aisera.service.llm;

import "google/protobuf/any.proto";

service LLMService {
  rpc FetchAnswer(LLMFetchAnswerRequest) returns (LLMFetchAnswerResponse);
  rpc FetchChatAnswer(LLMFetchChatAnswerRequest) returns (LLMFetchChatAnswerResponse);
  rpc StreamingAnswer(LLMStreamingAnswerRequest) returns (stream LLMStreamingAnswerResponse);
}
```

### Message Types

```protobuf
message PromptParam {
  string name = 1;
  google.protobuf.Any value = 2;
}

message ChatMessage {
  string role = 1;
  string content = 2;
  ContentType content_type = 3;
  FunctionCall function_call = 4;

  enum ContentType {
    TEXT = 0;
    IMAGE = 1;
    FUNCTION_CALL = 2;
  }
}

message FunctionDefinition {
  string name = 1;
  string description = 2;
  FunctionParameters parameters = 3;
}

message FunctionParameters {
  string type = 1;
  map<string, ParameterDefinition> properties = 2;
  repeated string required = 3;
}

message ParameterDefinition {
  string type = 1;
  string description = 2;
}

message FunctionCall {
  string name = 1;
  string arguments = 2;
}

message LLMFetchAnswerRequest {
  string tenant_id = 1;
  string prompt_name = 2;
  repeated PromptParam request_params = 3;
  map<string, google.protobuf.Any> config = 4;
  bool is_debug = 5;
  int64 bot_id = 6;
  string prompt_group_name = 7;
  bool use_cache = 8;
  bool detect_prompt_injection = 9;
}

message LLMFetchAnswerResponse {
  int32 status_code = 1;
  string error_message = 2;
  repeated PromptParam response_params = 3;
  repeated LLMDebugInfo llm_debug_infos = 4;
}

message LLMFetchChatAnswerRequest {
  string tenant_id = 1;
  string prompt_name = 2;
  repeated PromptParam request_params = 3;
  repeated ChatMessage messages = 4;
  map<string, google.protobuf.Any> config = 5;
  bool is_debug = 6;
  int64 bot_id = 7;
  repeated FunctionDefinition function_definitions = 8;
  string prompt_group_name = 9;
  bool use_cache = 10;
  bool detect_prompt_injection = 11;
}

message LLMFetchChatAnswerResponse {
  int32 status_code = 1;
  string error_message = 2;
  string error_code = 3;
  string message = 4;
  repeated PromptParam response_params = 5;
  repeated LLMDebugInfo llm_debug_infos = 6;
}

message LLMStreamingAnswerRequest {
  string tenant_id = 1;
  string prompt_name = 2;
  repeated PromptParam request_params = 3;
  repeated ChatMessage messages = 4;
  map<string, google.protobuf.Any> config = 5;
  int64 bot_id = 6;
  string prompt_group_name = 7;
}

message LLMStreamingAnswerResponse {
  string content = 1;
  bool is_done = 2;
}

message LLMDebugInfo {
  string tenant_id = 1;
  string prompt_group_name = 2;
  string prompt_name = 3;
  string applied_template = 4;
  repeated PromptParam request_params = 5;
  repeated PromptParam response_params = 6;
  string response_message = 7;
  int64 time_cost_in_millis = 8;
  map<string, google.protobuf.Any> config = 9;
  repeated ChatMessage messages = 10;
}
```

## Common Data Structures

### PromptParamDefinition

Defines a parameter for a prompt's inputs or outputs.

| Field | Type | Description |
|-------|------|-------------|
| name | string | Name of the parameter |
| type | string | Data type of the parameter (string, number, boolean, etc.) |
| description | string | Description of the parameter |
| required | boolean | Whether the parameter is required |
| defaultValue | string | Default value for the parameter |
| options | array of string | Possible values for the parameter (for enum types) |

### ChatMessage

Represents a message in a chat conversation.

| Field | Type | Description |
|-------|------|-------------|
| role | string | Role of the message sender (system, user, assistant) |
| content | string | Content of the message |
| contentType | string | Type of content (TEXT, IMAGE, FUNCTION_CALL) |
| function_call | object | Function call information (if contentType is FUNCTION_CALL) |

### FunctionDefinition

Defines a function that an LLM can call.

| Field | Type | Description |
|-------|------|-------------|
| name | string | Name of the function |
| description | string | Description of the function |
| parameters | object | Parameter schema for the function (JSON Schema object type) |

## Error Handling

The LLM Gateway returns standard HTTP status codes for REST API errors, along with error messages in the response body. For gRPC APIs, error information is included in the response message.

Common error codes:

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input parameters |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Prompt or LLM provider not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server-side error |
| 503 | Service Unavailable - LLM provider temporarily unavailable |

Example error response (REST):

```json
{
  "statusCode": 400,
  "errorMessage": "Prompt name cannot be empty",
  "errorCode": "VALIDATION_ERROR"
}
```