# Getting Started with the LLM Gateway API

This guide will help you get started with the LLM Gateway API, covering prerequisites, installation, and basic configuration.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [HTTP Clients](#http-clients)
  - [Language-Specific Libraries](#language-specific-libraries)
- [Configuration](#configuration)
  - [Base URLs](#base-urls)
  - [Timeouts](#timeouts)
  - [Logging](#logging)
- [Your First API Call](#your-first-api-call)

## Prerequisites

Before integrating with the LLM Gateway API, ensure you have the following:

1. **API Credentials**: An API key or authentication token (See the [Authentication guide](./authentication.md))
2. **HTTP Client**: A tool or library capable of making HTTP requests
3. **Environment Access**: Network access to the LLM Gateway API endpoints

### Supported Languages and Frameworks

The LLM Gateway API can be accessed from any language or framework that can make HTTP requests or gRPC calls. Here are some commonly used options:

| Language | Recommended Libraries |
|----------|----------------------|
| Python   | requests, httpx, grpcio |
| JavaScript/Node.js | axios, fetch, node-fetch, @grpc/grpc-js |
| Java     | OkHttp, Apache HttpClient, gRPC-Java |
| Go       | net/http, gRPC-Go |
| C#       | HttpClient, RestSharp, Grpc.Net.Client |

## Installation & Setup

### HTTP Clients

#### Python

```bash
pip install requests
```

```python
import requests

def llm_gateway_client(api_key):
    return requests.Session()
```

#### JavaScript/Node.js

```bash
npm install axios
```

```javascript
const axios = require('axios');

function llmGatewayClient(apiKey) {
  return axios.create({
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    }
  });
}
```

#### Java

```xml
<!-- Maven -->
<dependency>
    <groupId>com.squareup.okhttp3</groupId>
    <artifactId>okhttp</artifactId>
    <version>4.10.0</version>
</dependency>
```

```java
import okhttp3.OkHttpClient;
import okhttp3.Request;

public class LLMGatewayClient {
    private final OkHttpClient client;
    private final String apiKey;
    
    public LLMGatewayClient(String apiKey) {
        this.apiKey = apiKey;
        this.client = new OkHttpClient.Builder()
            .build();
    }
    
    // Methods for API calls will be added here
}
```

### Language-Specific Libraries

For a more streamlined experience, we offer the following official client libraries:

#### Python SDK

```bash
pip install aisera-llm-gateway-client
```

```python
from aisera.llm_gateway import LLMGatewayClient

client = LLMGatewayClient(api_key="your_api_key")
```

#### JavaScript/Node.js SDK

```bash
npm install @aisera/llm-gateway-client
```

```javascript
const { LLMGatewayClient } = require('@aisera/llm-gateway-client');

const client = new LLMGatewayClient({
  apiKey: 'your_api_key'
});
```

#### Java SDK

```xml
<dependency>
    <groupId>com.aisera</groupId>
    <artifactId>llm-gateway-client</artifactId>
    <version>1.0.0</version>
</dependency>
```

```java
import com.aisera.llm.gateway.LLMGatewayClient;

LLMGatewayClient client = new LLMGatewayClient.Builder()
    .apiKey("your_api_key")
    .build();
```

## Configuration

### Base URLs

Configure your client with the appropriate base URL for your environment:

| Environment | Base URL |
|-------------|----------|
| Production  | `https://api.aisera.com/llm/v1` |
| Staging     | `https://api-staging.aisera.com/llm/v1` |
| Development | `https://api-dev.aisera.com/llm/v1` |

Example configuration for different languages:

#### Python

```python
from aisera.llm_gateway import LLMGatewayClient

client = LLMGatewayClient(
    api_key="your_api_key",
    base_url="https://api.aisera.com/llm/v1"
)
```

#### JavaScript/Node.js

```javascript
const { LLMGatewayClient } = require('@aisera/llm-gateway-client');

const client = new LLMGatewayClient({
  apiKey: 'your_api_key',
  baseUrl: 'https://api.aisera.com/llm/v1'
});
```

#### Java

```java
import com.aisera.llm.gateway.LLMGatewayClient;

LLMGatewayClient client = new LLMGatewayClient.Builder()
    .apiKey("your_api_key")
    .baseUrl("https://api.aisera.com/llm/v1")
    .build();
```

### Timeouts

LLM operations can sometimes take longer than typical API calls. Configure appropriate timeouts to prevent premature request failures:

#### Python

```python
import requests

session = requests.Session()
session.request_timeout = 60  # 60 seconds
```

#### JavaScript/Node.js

```javascript
const axios = require('axios');

const client = axios.create({
  timeout: 60000  // 60 seconds in milliseconds
});
```

#### Java

```java
import okhttp3.OkHttpClient;
import java.util.concurrent.TimeUnit;

OkHttpClient client = new OkHttpClient.Builder()
    .connectTimeout(10, TimeUnit.SECONDS)
    .writeTimeout(10, TimeUnit.SECONDS)
    .readTimeout(60, TimeUnit.SECONDS)  // Longer read timeout for LLM responses
    .build();
```

### Logging

Enable logging to help debug API interactions:

#### Python

```python
import logging
logging.basicConfig(level=logging.INFO)
```

#### JavaScript/Node.js

```javascript
const { LLMGatewayClient } = require('@aisera/llm-gateway-client');

const client = new LLMGatewayClient({
  apiKey: 'your_api_key',
  logLevel: 'info'  // 'debug', 'info', 'warn', 'error'
});
```

#### Java

```java
import java.util.logging.Level;
import java.util.logging.Logger;

Logger logger = Logger.getLogger("com.aisera.llm.gateway");
logger.setLevel(Level.INFO);
```

## Your First API Call

Let's make a simple API call to check if the LLM Gateway is accessible:

### Health Check

#### cURL

```bash
curl -X GET https://api.aisera.com/llm/v1/health \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Python

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com/llm/v1"

response = requests.get(
    f"{base_url}/health",
    headers={"Authorization": f"Bearer {api_key}"}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

#### JavaScript/Node.js

```javascript
const axios = require('axios');

const apiKey = 'YOUR_API_KEY';
const baseUrl = 'https://api.aisera.com/llm/v1';

async function checkHealth() {
  try {
    const response = await axios.get(`${baseUrl}/health`, {
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    });
    
    console.log(`Status: ${response.status}`);
    console.log(`Response: ${JSON.stringify(response.data)}`);
  } catch (error) {
    console.error('Error checking health:', error.message);
  }
}

checkHealth();
```

### Execute a Simple Prompt

Here's how to execute a simple prompt using the LLM Gateway API:

#### cURL

```bash
curl -X POST https://api.aisera.com/llm/v1/execution/fetchChatAnswer \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tenantId": "9000",
    "promptName": "simple-qa",
    "requestParams": [
      {
        "name": "query",
        "value": "What is the capital of France?"
      }
    ],
    "botId": 123,
    "useCache": true
  }'
```

#### Python

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com/llm/v1"

payload = {
    "tenantId": "9000",
    "promptName": "simple-qa",
    "requestParams": [
        {
            "name": "query",
            "value": "What is the capital of France?"
        }
    ],
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

#### JavaScript/Node.js

```javascript
const axios = require('axios');

const apiKey = 'YOUR_API_KEY';
const baseUrl = 'https://api.aisera.com/llm/v1';

async function executePrompt() {
  try {
    const payload = {
      tenantId: '9000',
      promptName: 'simple-qa',
      requestParams: [
        {
          name: 'query',
          value: 'What is the capital of France?'
        }
      ],
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
    console.error('Error executing prompt:', error.message);
  }
}

executePrompt();
```

Now you're ready to start integrating with the LLM Gateway API! Proceed to the other sections of this guide to learn more about authentication, available endpoints, and best practices.