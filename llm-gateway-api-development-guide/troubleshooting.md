# Troubleshooting & FAQs

This guide provides solutions to common issues you might encounter when using the LLM Gateway API, along with frequently asked questions.

## Table of Contents

- [Common Issues](#common-issues)
  - [Authentication Problems](#authentication-problems)
  - [Rate Limiting](#rate-limiting)
  - [Prompt Execution Failures](#prompt-execution-failures)
  - [Request Validation Errors](#request-validation-errors)
  - [Token Limits](#token-limits)
  - [Timeout Errors](#timeout-errors)
- [Debugging Techniques](#debugging-techniques)
  - [Request Inspection](#request-inspection)
  - [Response Analysis](#response-analysis)
  - [Logging Best Practices](#logging-best-practices)
- [Performance Optimization](#performance-optimization)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Support Resources](#support-resources)

## Common Issues

### Authentication Problems

#### Issue: 401 Unauthorized Error

**Possible Causes:**
- Invalid API key
- Expired API key
- Incorrect authorization header format

**Solutions:**
1. Verify your API key is correct and hasn't expired
2. Ensure the Authorization header is formatted correctly: `Authorization: Bearer YOUR_API_KEY`
3. Check if your API key has the necessary permissions for the requested operation

#### Issue: 403 Forbidden Error

**Possible Causes:**
- Insufficient permissions for the requested operation
- API key restricted to specific IP addresses
- Tenant ID mismatch

**Solutions:**
1. Verify that your API key has the required permissions (e.g., `llm:read`, `llm:write`, `llm:admin`)
2. Check if your API key has IP restrictions and ensure your requests come from allowed IPs
3. Verify you're using the correct tenant ID for your organization

### Rate Limiting

#### Issue: 429 Too Many Requests Error

**Possible Causes:**
- Exceeded rate limits for your plan
- Too many concurrent requests
- Unevenly distributed requests causing spikes

**Solutions:**
1. Implement retry logic with exponential backoff (use the `Retry-After` header value)
2. Monitor your usage with the quota endpoints
3. Distribute requests more evenly over time
4. Consider upgrading your plan for higher limits

**Example Retry Implementation:**

```javascript
async function makeRequestWithRetry(url, options, maxRetries = 5) {
  let retries = 0;
  
  while (retries < maxRetries) {
    try {
      const response = await fetch(url, options);
      
      if (response.status !== 429) {
        return response;
      }
      
      // Get retry-after header (in seconds) or default to exponential backoff
      const retryAfter = parseInt(response.headers.get('Retry-After') || Math.pow(2, retries));
      console.log(`Rate limited. Retrying after ${retryAfter} seconds.`);
      
      // Wait for the specified time
      await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
      retries++;
      
    } catch (error) {
      if (retries === maxRetries - 1) throw error;
      retries++;
    }
  }
}
```

### Prompt Execution Failures

#### Issue: Model-Specific Failures

**Possible Causes:**
- Model doesn't support the requested capabilities
- Model is temporarily unavailable
- Input text violates model's content policy

**Solutions:**
1. Check model capabilities in the LLM Registry before using
2. Implement fallback to alternative models
3. Review content policy and ensure inputs comply

#### Issue: Context Length Exceeded

**Possible Causes:**
- Input prompt exceeds the model's maximum token limit

**Solutions:**
1. Use a model with a larger context window
2. Implement chunking and summarization techniques
3. Optimize your prompts to be more concise

**Example Code to Check Token Count:**

```python
from aisera.llm_gateway import LLMGatewayClient
from aisera.llm_gateway.utils import count_tokens

client = LLMGatewayClient(
    api_key="YOUR_API_KEY",
    tenant_id="YOUR_TENANT_ID"
)

def execute_with_token_check(prompt, model="gpt-4"):
    # Get model info to check context limit
    model_info = client.get_model(model)
    max_tokens = model_info.context_window
    
    # Count tokens in prompt
    token_count = count_tokens(prompt, model)
    print(f"Prompt token count: {token_count}")
    
    if token_count > max_tokens:
        raise ValueError(f"Prompt exceeds token limit ({token_count} > {max_tokens})")
    
    # Execute prompt
    return client.execute_prompt(prompt=prompt, model=model)
```

### Request Validation Errors

#### Issue: 400 Bad Request with Validation Errors

**Possible Causes:**
- Missing required parameters
- Parameter type mismatch
- Invalid parameter format

**Solutions:**
1. Check the `error.details` field in the response for specific validation errors
2. Validate request payloads against the API schemas before sending
3. Use the SDKs which include built-in validation

### Token Limits

#### Issue: Exceeded Monthly Token Quota

**Possible Causes:**
- Used all allocated tokens for the current period
- Unexpected usage spike

**Solutions:**
1. Monitor your token usage proactively using the quota endpoints
2. Implement token budget management in your application
3. Request a temporary quota increase for unexpected needs

### Timeout Errors

#### Issue: 504 Gateway Timeout

**Possible Causes:**
- Model is taking too long to generate a response
- Complex prompt requiring extensive processing
- System under heavy load

**Solutions:**
1. Simplify your prompts or break them into smaller steps
2. Adjust the timeout parameter in your requests
3. Consider using a different, faster model for time-sensitive operations
4. Implement asynchronous processing for non-interactive use cases

## Debugging Techniques

### Request Inspection

For systematic debugging, capture the full request details:

```python
import requests
import json

def debug_request(method, url, headers, data=None):
    # Print request details
    print(f"\n---- REQUEST ----")
    print(f"{method} {url}")
    print("\nHeaders:")
    for key, value in headers.items():
        # Mask sensitive information
        if key.lower() == 'authorization':
            print(f"{key}: Bearer ***")
        else:
            print(f"{key}: {value}")
    
    if data:
        print("\nPayload:")
        print(json.dumps(data, indent=2))
    
    # Make the request
    if method.lower() == 'get':
        response = requests.get(url, headers=headers)
    else:
        response = requests.post(url, headers=headers, json=data)
    
    # Print response details
    print(f"\n---- RESPONSE ----")
    print(f"Status: {response.status_code}")
    print("\nHeaders:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    
    try:
        print("\nBody:")
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    
    return response

# Example usage
debug_request(
    'POST',
    'https://api.aisera.com/v1/tenants/9000/llm/execute',
    {
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    {
        'prompt': 'Explain quantum computing',
        'model': 'gpt-4'
    }
)
```

### Response Analysis

When debugging issues, always examine:

1. **HTTP Status Code**: Indicates the general category of the response
2. **Response Headers**: Contain metadata like rate limit information
3. **Error Object**: Contains detailed error information
4. **Request ID**: Essential for support inquiries

### Logging Best Practices

Implement structured logging for API interactions:

```javascript
const winston = require('winston');
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  defaultMeta: { service: 'llm-gateway-client' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

function logApiInteraction(requestData, responseData, error = null) {
  // Create a sanitized copy of request data (remove sensitive info)
  const sanitizedRequest = { ...requestData };
  if (sanitizedRequest.headers && sanitizedRequest.headers.Authorization) {
    sanitizedRequest.headers.Authorization = 'Bearer ***';
  }
  
  const logData = {
    timestamp: new Date().toISOString(),
    request: sanitizedRequest,
    response: responseData ? {
      status: responseData.status,
      headers: responseData.headers,
      requestId: responseData.data?.error?.request_id,
      errorCode: responseData.data?.error?.code
    } : null,
    error: error ? {
      message: error.message,
      stack: error.stack
    } : null
  };
  
  if (error || (responseData && responseData.status >= 400)) {
    logger.error('API Error', logData);
  } else {
    logger.info('API Request', logData);
  }
  
  // Always log the request ID if available
  if (responseData?.data?.error?.request_id) {
    console.log(`Request ID: ${responseData.data.error.request_id}`);
  }
}
```

## Performance Optimization

### Reducing Latency

1. **Use the closest region endpoint**:
   - US: `https://us-api.aisera.com`
   - EU: `https://eu-api.aisera.com`
   - APAC: `https://ap-api.aisera.com`

2. **Optimize prompt length**:
   - Remove unnecessary context
   - Use reference pointers instead of embedding large texts

3. **Select appropriate models**:
   - Faster models for interactive use cases
   - More powerful models for complex reasoning

4. **Implement request caching**:
   - Cache identical prompt executions
   - Use sensible cache expiration times
   - Consider semantic caching for similar prompts

5. **Use connection pooling**:
   - Maintain persistent HTTP connections
   - Configure appropriate keepalive settings

### Batch Processing

For processing large numbers of prompts:

1. **Use parallel processing with rate limiting**:
   - Control concurrency based on your rate limits
   - Implement proper error handling and retries

2. **Consider asynchronous workflows**:
   - Submit batch jobs
   - Poll for results or use webhooks

## Frequently Asked Questions

### General Questions

**Q: How is the token usage calculated?**
A: Token usage is calculated based on the tokenization algorithm of the specific LLM model. Both input and output tokens are counted. The API returns the token counts in the response metadata.

**Q: How can I estimate token usage before making a request?**
A: Use the token counting utilities in our SDKs to estimate usage:

```python
from aisera.llm_gateway.utils import count_tokens

prompt = "This is a test prompt"
token_count = count_tokens(prompt, model="gpt-4")
print(f"Estimated token count: {token_count}")
```

**Q: Can I execute prompts in languages other than English?**
A: Yes, the LLM Gateway supports multi-language prompts. Models vary in their multilingual capabilities, so check the model documentation for specific language support.

**Q: How can I ensure consistent results across multiple calls?**
A: Set a consistent `temperature` value (lower for more deterministic outputs) and use the `seed` parameter to get reproducible results:

```javascript
const response = await client.executePrompt({
  prompt: "Explain quantum computing",
  model: "gpt-4",
  temperature: 0.0,
  seed: 12345  // Fixed seed for reproducibility
});
```

### Prompt Management

**Q: How can I organize prompts by category or project?**
A: Use tags when creating prompts:

```python
client.create_prompt(
    name="Customer Inquiry Response",
    template="...",
    tags=["customer-service", "project-alpha"]
)

# Later, filter by tags
prompts = client.list_prompts(tags=["project-alpha"])
```

**Q: What's the best practice for managing prompt versions in a team?**
A: Follow these practices:
1. Always create new versions for changes instead of editing existing ones
2. Use descriptive comments when creating versions
3. Test draft versions before publishing
4. Use version control systems for prompt templates

### Security

**Q: How can I restrict what my API key can access?**
A: API keys can be configured with specific scopes and permission levels in the developer portal. You can create keys with read-only access, prompt execution only, or full administrative access.

**Q: Is data encrypted in transit and at rest?**
A: Yes, all data is encrypted in transit using TLS, and at rest using AES-256 encryption.

**Q: How long is my data retained?**
A: By default, prompt inputs and outputs are retained for 30 days for billing and debugging purposes. You can configure shorter retention periods or opt for immediate deletion in compliance settings.

### Billing

**Q: How does billing work for token usage?**
A: Billing is based on the total token count (input + output) for each model. Different models have different pricing tiers. You can view your current usage and projected costs in the billing dashboard.

**Q: What happens if I exceed my plan's quota?**
A: Behavior depends on your plan settings:
- Free tier: Requests are rejected with 429 status when limits are reached
- Paid plans: By default, you'll be billed for overages at the standard rate
- Enterprise plans: Customizable overage behavior and notifications

## Support Resources

### Documentation

- [API Reference](https://api.aisera.com/docs)
- [SDK Documentation](https://api.aisera.com/docs/sdks)
- [Tutorials](https://api.aisera.com/docs/tutorials)

### Support Channels

- **Email Support**: support@aisera.com
- **Developer Forum**: [https://community.aisera.com](https://community.aisera.com)
- **GitHub Issues** (for SDK bugs): [https://github.com/aisera/llm-gateway-sdk/issues](https://github.com/aisera/llm-gateway-sdk/issues)

### Priority Support

Enterprise customers have access to priority support with:
- Dedicated support contacts
- 24/7 emergency support
- 1-hour response SLA for critical issues

Contact your account manager to enable priority support.

### Support Information to Include

When contacting support, always include:
- Request ID from the error response
- API endpoint and method
- HTTP status code
- Error code and message
- Timestamp of the issue
- Steps to reproduce the problem