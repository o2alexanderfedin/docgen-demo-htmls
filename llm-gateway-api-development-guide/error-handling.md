# Error Handling & Status Codes

This document describes how the LLM Gateway API handles errors and provides guidance on interpreting and handling error responses in your applications.

## Table of Contents

- [Overview](#overview)
- [Error Response Format](#error-response-format)
- [HTTP Status Codes](#http-status-codes)
- [Error Types](#error-types)
- [Handling Errors](#handling-errors)
- [Rate Limiting Errors](#rate-limiting-errors)
- [Code Examples](#code-examples)

## Overview

The LLM Gateway API uses conventional HTTP response codes to indicate the success or failure of API requests. In general:

- Codes in the `2xx` range indicate success
- Codes in the `4xx` range indicate an error caused by the client (e.g., invalid parameters, authentication issues)
- Codes in the `5xx` range indicate an error on the server side

All error responses include a structured JSON body with detailed information to help you identify and resolve the issue.

## Error Response Format

Error responses follow a consistent format:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "The request was malformed or invalid",
    "details": [
      {
        "field": "prompt",
        "issue": "required",
        "message": "Prompt parameter is required"
      }
    ],
    "request_id": "req_ab12cd34ef56"
  }
}
```

The error object contains:

| Field | Description |
|-------|-------------|
| code | A string identifier for the error type |
| message | A human-readable description of the error |
| details | An array of detailed information, often identifying specific fields with issues |
| request_id | A unique identifier for the request, useful when contacting support |

## HTTP Status Codes

The LLM Gateway API uses the following HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| 200 OK | The request was successful |
| 201 Created | The resource was successfully created |
| 400 Bad Request | The request was invalid or malformed |
| 401 Unauthorized | Authentication credentials were missing or invalid |
| 403 Forbidden | The authenticated user doesn't have permission for the requested operation |
| 404 Not Found | The requested resource was not found |
| 409 Conflict | The request conflicts with the current state of the resource |
| 422 Unprocessable Entity | The request was well-formed but contains semantic errors |
| 429 Too Many Requests | The client has sent too many requests in a given time period |
| 500 Internal Server Error | An error occurred on the server |
| 503 Service Unavailable | The service is temporarily unavailable |

## Error Types

Common error codes you may encounter:

| Error Code | Description |
|------------|-------------|
| authentication_error | Issues with authentication credentials |
| authorization_error | Permission-related issues |
| invalid_request | General validation errors |
| parameter_error | Issues with specific parameters |
| resource_not_found | The requested resource doesn't exist |
| rate_limit_exceeded | Client exceeded rate limits |
| model_error | Issues with the requested LLM model |
| provider_error | Issues with the LLM provider service |
| version_conflict | Resource version conflict |
| internal_error | Server-side issues |

## Handling Errors

### Best Practices

1. **Check the HTTP status code first** to understand the general category of the error
2. **Read the error.code field** to identify the specific error type
3. **Examine the error.details array** for field-specific issues
4. **Log the request_id** for troubleshooting purposes
5. **Implement retry logic** with exponential backoff for 429 and 5xx errors
6. **Display user-friendly error messages** in your application

### Validation Errors

For 400 Bad Request errors, check the `details` array for specific field issues. Each detail includes:

- `field`: The name of the problematic field
- `issue`: The type of validation issue (e.g., "required", "invalid_format")
- `message`: A descriptive message about the issue

### Authentication Errors

For 401 Unauthorized errors, verify that:

- Your API key is correctly formatted
- Your authorization header is correctly structured
- Your API key has not expired or been revoked

## Rate Limiting Errors

The LLM Gateway implements rate limiting to ensure fair usage and system stability. When you exceed these limits, you'll receive a 429 Too Many Requests error.

Rate limit response headers:

| Header | Description |
|--------|-------------|
| X-RateLimit-Limit | The maximum number of requests allowed in the current time window |
| X-RateLimit-Remaining | The number of requests remaining in the current time window |
| X-RateLimit-Reset | The time (in seconds) when the current rate limit window resets |

When receiving a 429 error, implement a backoff strategy before retrying. The response will include a `Retry-After` header indicating the recommended wait time in seconds.

## Code Examples

### Handling Errors in Python

```python
import requests
import time

def make_api_request(url, headers, data=None, max_retries=3):
    retries = 0
    base_delay = 1  # Starting delay in seconds
    
    while retries < max_retries:
        try:
            if data:
                response = requests.post(url, headers=headers, json=data)
            else:
                response = requests.get(url, headers=headers)
            
            # Successful response
            if response.status_code >= 200 and response.status_code < 300:
                return response.json()
            
            # Rate limiting - implement backoff
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', base_delay * (2 ** retries)))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
                retries += 1
                continue
            
            # Server errors - retry with backoff
            if response.status_code >= 500:
                delay = base_delay * (2 ** retries)
                print(f"Server error. Retrying after {delay} seconds.")
                time.sleep(delay)
                retries += 1
                continue
            
            # Client errors - parse the error and return it
            error_data = response.json()
            request_id = error_data.get('error', {}).get('request_id', 'unknown')
            error_code = error_data.get('error', {}).get('code', 'unknown')
            error_message = error_data.get('error', {}).get('message', 'Unknown error')
            
            print(f"API Error: {error_message} (Code: {error_code}, Request ID: {request_id})")
            
            # Format field errors for display
            if 'details' in error_data.get('error', {}):
                for detail in error_data['error']['details']:
                    field = detail.get('field', '')
                    message = detail.get('message', '')
                    print(f"  - {field}: {message}")
            
            return error_data
            
        except Exception as e:
            delay = base_delay * (2 ** retries)
            print(f"Request exception: {str(e)}. Retrying after {delay} seconds.")
            time.sleep(delay)
            retries += 1
    
    raise Exception(f"Failed after {max_retries} retries")

# Example usage
api_key = "YOUR_API_KEY"
url = "https://api.aisera.com/v1/tenants/9000/llm/execute"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "prompt": "Explain quantum computing in simple terms",
    "model": "gpt-4"
}

response = make_api_request(url, headers, data)
print(response)
```

### Handling Errors in JavaScript

```javascript
const axios = require('axios');

async function makeApiRequest(url, headers, data = null, maxRetries = 3) {
  let retries = 0;
  const baseDelay = 1000; // Starting delay in milliseconds
  
  while (retries < maxRetries) {
    try {
      const config = {
        headers,
        validateStatus: null // Don't throw errors for non-2xx responses
      };
      
      const response = data 
        ? await axios.post(url, data, config)
        : await axios.get(url, config);
      
      // Successful response
      if (response.status >= 200 && response.status < 300) {
        return response.data;
      }
      
      // Rate limiting - implement backoff
      if (response.status === 429) {
        const retryAfter = parseInt(response.headers['retry-after'] || baseDelay * Math.pow(2, retries) / 1000);
        console.log(`Rate limit exceeded. Retrying after ${retryAfter} seconds.`);
        await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
        retries++;
        continue;
      }
      
      // Server errors - retry with backoff
      if (response.status >= 500) {
        const delay = baseDelay * Math.pow(2, retries);
        console.log(`Server error. Retrying after ${delay / 1000} seconds.`);
        await new Promise(resolve => setTimeout(resolve, delay));
        retries++;
        continue;
      }
      
      // Client errors - parse the error and return it
      const errorData = response.data;
      const requestId = errorData?.error?.request_id || 'unknown';
      const errorCode = errorData?.error?.code || 'unknown';
      const errorMessage = errorData?.error?.message || 'Unknown error';
      
      console.log(`API Error: ${errorMessage} (Code: ${errorCode}, Request ID: ${requestId})`);
      
      // Format field errors for display
      if (errorData?.error?.details) {
        errorData.error.details.forEach(detail => {
          const field = detail.field || '';
          const message = detail.message || '';
          console.log(`  - ${field}: ${message}`);
        });
      }
      
      return errorData;
      
    } catch (error) {
      const delay = baseDelay * Math.pow(2, retries);
      console.log(`Request exception: ${error.message}. Retrying after ${delay / 1000} seconds.`);
      await new Promise(resolve => setTimeout(resolve, delay));
      retries++;
    }
  }
  
  throw new Error(`Failed after ${maxRetries} retries`);
}

// Example usage
const apiKey = 'YOUR_API_KEY';
const url = 'https://api.aisera.com/v1/tenants/9000/llm/execute';

const headers = {
  'Authorization': `Bearer ${apiKey}`,
  'Content-Type': 'application/json'
};

const data = {
  prompt: 'Explain quantum computing in simple terms',
  model: 'gpt-4'
};

makeApiRequest(url, headers, data)
  .then(response => console.log(response))
  .catch(error => console.error('Failed to make API request:', error.message));
```