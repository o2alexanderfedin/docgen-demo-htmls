# Rate Limits & Throttling

This document explains the rate limiting policies and throttling mechanisms implemented in the LLM Gateway API to ensure fair usage and system stability.

## Table of Contents

- [Overview](#overview)
- [Rate Limit Categories](#rate-limit-categories)
- [Rate Limit Headers](#rate-limit-headers)
- [Best Practices](#best-practices)
- [Request Costs](#request-costs)
- [Quota Management](#quota-management)
- [Error Handling](#error-handling)
- [Implementation Examples](#implementation-examples)

## Overview

The LLM Gateway API implements rate limiting to:

- Ensure fair distribution of resources among all clients
- Protect the service from abuse and overwhelming traffic
- Maintain optimal performance and reliability

When you exceed a rate limit, the API will return a `429 Too Many Requests` status code with information about when you can resume making requests.

## Rate Limit Categories

Rate limits are divided into several categories, each with its own limits and quotas:

### 1. Global Rate Limits

Applied to all API requests across all endpoints:

| Plan | Requests per Minute | Requests per Day |
|------|---------------------|------------------|
| Developer | 60 | 10,000 |
| Business | 300 | 100,000 |
| Enterprise | 1,000 | 1,000,000 |
| Custom | Customized based on needs | Customized based on needs |

### 2. Endpoint-Specific Rate Limits

Different endpoints have different resource costs:

| Endpoint Category | Requests per Minute | Notes |
|-------------------|---------------------|-------|
| Prompt Execution | 30 | Higher cost operations |
| LLM Registry | 120 | Read-heavy operations |
| Prompt Management | 60 | Mixed read/write operations |
| Versioning | 60 | Version management operations |

### 3. Model-Specific Rate Limits

Some models have specific rate limits due to their computational requirements:

| Model | Tokens per Minute | Requests per Minute |
|-------|-------------------|---------------------|
| GPT-4 | 10,000 | 20 |
| GPT-3.5-Turbo | 100,000 | 60 |
| Claude-3-Opus | 30,000 | 30 |
| Claude-3-Sonnet | 80,000 | 50 |
| Llama-2-70B | 50,000 | 40 |

### 4. Tenant-Specific Rate Limits

Multi-tenant usage is subject to tenant-specific quotas:

| Tenant Tier | Requests per Minute | Monthly Token Quota |
|-------------|---------------------|---------------------|
| Basic | 60 | 1,000,000 |
| Standard | 300 | 10,000,000 |
| Premium | 600 | 50,000,000 |

## Rate Limit Headers

The API includes the following headers in responses to help you track your rate limit usage:

| Header | Description |
|--------|-------------|
| X-RateLimit-Limit | The maximum number of requests you can make per time window |
| X-RateLimit-Remaining | The number of requests remaining in the current time window |
| X-RateLimit-Reset | The time (in seconds) when the current rate limit window resets |
| X-RateLimit-Type | The type of rate limit that is currently being tracked (global, endpoint, model) |

When a rate limit is exceeded, the response will include:

| Header | Description |
|--------|-------------|
| Retry-After | The number of seconds to wait before making another request |

## Best Practices

To avoid hitting rate limits, follow these best practices:

### 1. Implement Client-Side Rate Limiting

Design your applications to respect rate limits by:

- Tracking rate limit headers in responses
- Implementing retry mechanisms with exponential backoff
- Distributing requests evenly over time
- Batch processing requests when possible

### 2. Optimize Request Usage

Reduce unnecessary API calls:

- Cache responses when appropriate
- Consolidate multiple small requests into batch operations
- Use webhooks for event notifications instead of polling
- Implement request debouncing and throttling in your client application

### 3. Monitor Usage

Keep track of your API usage:

- Use the quota management endpoints to monitor your usage
- Set up alerts when approaching rate limits
- Review usage patterns to identify optimization opportunities

## Request Costs

Not all requests have the same "cost" in terms of rate limits. The system uses a cost-based approach:

| Operation | Base Cost | Factors Affecting Cost |
|-----------|-----------|------------------------|
| Prompt Execution | 1-10 | Model complexity, input tokens, output tokens |
| Prompt Management | 1-2 | Request size, complexity |
| Versioning | 1 | Standard cost |
| LLM Registry | 1 | Standard cost |

For prompt execution, costs are calculated based on:
- Base cost for the chosen model
- Input token count / 1000
- Output token cost based on model and generation parameters

Example:
```
Request Cost = Base Model Cost + (Input Tokens / 1000) + Output Token Cost
```

## Quota Management

The API provides endpoints to help you manage your quotas:

### Check Current Usage

```
GET /v1/tenants/{tenantId}/quotas/usage
```

Returns your current usage metrics across all categories.

### Sample Response

```json
{
  "current_period": {
    "start": "2023-09-01T00:00:00Z",
    "end": "2023-09-30T23:59:59Z"
  },
  "limits": {
    "requests": {
      "limit": 100000,
      "used": 45230,
      "remaining": 54770
    },
    "tokens": {
      "limit": 10000000,
      "used": 3245600,
      "remaining": 6754400
    }
  },
  "models": {
    "gpt-4": {
      "tokens": {
        "limit": 1000000,
        "used": 420500,
        "remaining": 579500
      }
    },
    "claude-3-opus": {
      "tokens": {
        "limit": 2000000,
        "used": 890300,
        "remaining": 1109700
      }
    }
  }
}
```

### Request Quota Increase

For temporary quota increases:

```
POST /v1/tenants/{tenantId}/quotas/increase
```

With body:

```json
{
  "quota_type": "tokens",
  "model": "gpt-4",
  "amount": 500000,
  "justification": "Temporary increase needed for batch processing project",
  "duration_days": 7
}
```

## Error Handling

When you exceed a rate limit, you'll receive a `429 Too Many Requests` response with the following body:

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "You have exceeded the rate limit for prompt execution requests",
    "details": {
      "limit_type": "requests_per_minute",
      "limit": 30,
      "reset_at": "2023-09-15T10:15:00Z"
    },
    "request_id": "req_ab12cd34ef56"
  }
}
```

### Handling Rate Limit Errors

1. **Implement Exponential Backoff**: When you receive a 429 response, wait for the time specified in the `Retry-After` header before retrying.

2. **Scale Backoff with Consecutive Failures**: Increase the wait time exponentially if you continue to receive 429 responses.

3. **Consider Circuit Breakers**: Implement circuit breakers to temporarily disable API requests after multiple failures.

## Implementation Examples

### Python Example

```python
import requests
import time

class RateLimitHandler:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        # Track rate limits
        self.rate_limits = {
            "global": {"limit": 0, "remaining": 0, "reset": 0},
            "endpoint": {"limit": 0, "remaining": 0, "reset": 0},
            "model": {"limit": 0, "remaining": 0, "reset": 0}
        }
    
    def make_request(self, method, endpoint, data=None, max_retries=5):
        retries = 0
        base_delay = 1  # Starting delay in seconds
        
        while retries < max_retries:
            try:
                # Check if we should wait based on previous rate limit info
                self._wait_if_needed()
                
                # Make the request
                if method.lower() == "get":
                    response = requests.get(
                        f"{self.base_url}{endpoint}", 
                        headers=self.headers
                    )
                else:
                    response = requests.post(
                        f"{self.base_url}{endpoint}", 
                        headers=self.headers, 
                        json=data
                    )
                
                # Update rate limit tracking from headers
                self._update_rate_limits(response)
                
                # If successful, return the response
                if response.status_code < 300:
                    return response.json()
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', base_delay * (2 ** retries)))
                    print(f"Rate limit exceeded. Waiting {retry_after} seconds.")
                    time.sleep(retry_after)
                    retries += 1
                    continue
                
                # Handle other errors
                print(f"Error: {response.status_code} - {response.text}")
                return response.json()
                
            except Exception as e:
                delay = base_delay * (2 ** retries)
                print(f"Request exception: {str(e)}. Retrying after {delay} seconds.")
                time.sleep(delay)
                retries += 1
        
        raise Exception(f"Failed after {max_retries} retries")
    
    def _update_rate_limits(self, response):
        # Update our tracking of rate limits based on response headers
        if 'X-RateLimit-Type' in response.headers:
            limit_type = response.headers['X-RateLimit-Type']
            if limit_type in self.rate_limits:
                self.rate_limits[limit_type]['limit'] = int(response.headers.get('X-RateLimit-Limit', 0))
                self.rate_limits[limit_type]['remaining'] = int(response.headers.get('X-RateLimit-Remaining', 0))
                self.rate_limits[limit_type]['reset'] = int(response.headers.get('X-RateLimit-Reset', 0))
    
    def _wait_if_needed(self):
        # Check if we need to wait for any rate limits
        now = time.time()
        for limit_type, info in self.rate_limits.items():
            if info['remaining'] == 0 and info['reset'] > now:
                wait_time = info['reset'] - now
                print(f"Rate limit ({limit_type}) reached. Waiting {wait_time:.2f} seconds.")
                time.sleep(wait_time)

# Example usage
api_client = RateLimitHandler("https://api.aisera.com", "YOUR_API_KEY")

# Get prompt list
prompts = api_client.make_request("GET", "/v1/tenants/9000/llm/prompts")
print(f"Retrieved {len(prompts['items'])} prompts")

# Execute prompt
execution_result = api_client.make_request(
    "POST", 
    "/v1/tenants/9000/llm/execute",
    {
        "prompt": "Explain quantum computing in simple terms",
        "model": "gpt-4"
    }
)
print(execution_result)
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

class RateLimitHandler {
  constructor(baseUrl, apiKey) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
    this.headers = {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    };
    // Track rate limits
    this.rateLimits = {
      global: { limit: 0, remaining: 0, reset: 0 },
      endpoint: { limit: 0, remaining: 0, reset: 0 },
      model: { limit: 0, remaining: 0, reset: 0 }
    };
  }
  
  async makeRequest(method, endpoint, data = null, maxRetries = 5) {
    let retries = 0;
    const baseDelay = 1000; // Starting delay in milliseconds
    
    while (retries < maxRetries) {
      try {
        // Check if we should wait based on previous rate limit info
        await this._waitIfNeeded();
        
        // Make the request
        const config = {
          method: method.toLowerCase(),
          url: `${this.baseUrl}${endpoint}`,
          headers: this.headers,
          validateStatus: null // Don't throw on error status codes
        };
        
        if (data && method.toLowerCase() !== 'get') {
          config.data = data;
        }
        
        const response = await axios(config);
        
        // Update rate limit tracking from headers
        this._updateRateLimits(response);
        
        // If successful, return the response
        if (response.status < 300) {
          return response.data;
        }
        
        // Handle rate limiting
        if (response.status === 429) {
          const retryAfter = parseInt(response.headers['retry-after'] || baseDelay * Math.pow(2, retries) / 1000);
          console.log(`Rate limit exceeded. Waiting ${retryAfter} seconds.`);
          await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
          retries++;
          continue;
        }
        
        // Handle other errors
        console.log(`Error: ${response.status} - ${JSON.stringify(response.data)}`);
        return response.data;
        
      } catch (error) {
        const delay = baseDelay * Math.pow(2, retries);
        console.log(`Request exception: ${error.message}. Retrying after ${delay / 1000} seconds.`);
        await new Promise(resolve => setTimeout(resolve, delay));
        retries++;
      }
    }
    
    throw new Error(`Failed after ${maxRetries} retries`);
  }
  
  _updateRateLimits(response) {
    // Update our tracking of rate limits based on response headers
    const limitType = response.headers['x-ratelimit-type'];
    if (limitType && this.rateLimits[limitType]) {
      this.rateLimits[limitType].limit = parseInt(response.headers['x-ratelimit-limit'] || 0);
      this.rateLimits[limitType].remaining = parseInt(response.headers['x-ratelimit-remaining'] || 0);
      this.rateLimits[limitType].reset = parseInt(response.headers['x-ratelimit-reset'] || 0);
    }
  }
  
  async _waitIfNeeded() {
    // Check if we need to wait for any rate limits
    const now = Math.floor(Date.now() / 1000);
    for (const [limitType, info] of Object.entries(this.rateLimits)) {
      if (info.remaining === 0 && info.reset > now) {
        const waitTime = info.reset - now;
        console.log(`Rate limit (${limitType}) reached. Waiting ${waitTime} seconds.`);
        await new Promise(resolve => setTimeout(resolve, waitTime * 1000));
      }
    }
  }
}

// Example usage
async function main() {
  const apiClient = new RateLimitHandler('https://api.aisera.com', 'YOUR_API_KEY');
  
  try {
    // Get prompt list
    const prompts = await apiClient.makeRequest('GET', '/v1/tenants/9000/llm/prompts');
    console.log(`Retrieved ${prompts.items.length} prompts`);
    
    // Execute prompt
    const executionResult = await apiClient.makeRequest(
      'POST', 
      '/v1/tenants/9000/llm/execute',
      {
        prompt: 'Explain quantum computing in simple terms',
        model: 'gpt-4'
      }
    );
    console.log(executionResult);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

main();
```