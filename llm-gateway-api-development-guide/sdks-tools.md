# SDKs, Samples & Tools

This document provides information about the available SDKs, code samples, and tools that can help you integrate and work with the LLM Gateway API more efficiently.

## Table of Contents

- [Official SDKs](#official-sdks)
- [Code Samples](#code-samples)
- [Tools & Utilities](#tools--utilities)
- [Client Libraries](#client-libraries)
- [Community Resources](#community-resources)

## Official SDKs

The LLM Gateway provides official SDKs for several popular programming languages to simplify integration with your applications.

### Python SDK

The official Python SDK provides a convenient way to interact with the LLM Gateway API.

#### Installation

```bash
pip install aisera-llm-gateway-sdk
```

#### Basic Usage

```python
from aisera.llm_gateway import LLMGatewayClient

# Initialize the client
client = LLMGatewayClient(
    api_key="YOUR_API_KEY",
    tenant_id="YOUR_TENANT_ID"
)

# Execute a prompt
response = client.execute_prompt(
    prompt="Explain quantum computing in simple terms",
    model="gpt-4"
)

print(response.text)

# Create a new prompt template
new_prompt = client.create_prompt(
    name="Customer Service Response",
    description="Generate customer service responses for various scenarios",
    template="Please provide a professional customer service response to the following inquiry: {{inquiry}}",
    parameters={
        "inquiry": {
            "type": "string",
            "description": "The customer inquiry to respond to",
            "required": True
        }
    }
)

print(f"Created prompt with ID: {new_prompt.id}")
```

#### Advanced Features

The Python SDK supports all API features with convenience methods:

```python
# Working with prompt versions
versions = client.list_prompt_versions(prompt_id="pr_123456")
for version in versions:
    print(f"Version {version.version}: {version.status}")

# Publishing a version
client.publish_prompt_version(
    prompt_id="pr_123456",
    version_id="v_abc123"
)

# Working with model registry
models = client.list_models(provider="openai")
for model in models:
    print(f"{model.id}: {model.name} - {model.capabilities}")
```

#### Async Support

The SDK provides async versions of all methods:

```python
import asyncio
from aisera.llm_gateway.async_client import AsyncLLMGatewayClient

async def main():
    client = AsyncLLMGatewayClient(
        api_key="YOUR_API_KEY",
        tenant_id="YOUR_TENANT_ID"
    )
    
    # Execute multiple prompts concurrently
    tasks = [
        client.execute_prompt("Explain quantum computing", model="gpt-4"),
        client.execute_prompt("What is machine learning?", model="gpt-3.5-turbo"),
        client.execute_prompt("How does blockchain work?", model="claude-3-sonnet")
    ]
    
    responses = await asyncio.gather(*tasks)
    for i, response in enumerate(responses):
        print(f"Response {i+1}: {response.text[:100]}...")
    
    await client.close()

asyncio.run(main())
```

### JavaScript/TypeScript SDK

The JavaScript/TypeScript SDK works in both Node.js and browser environments.

#### Installation

```bash
npm install @aisera/llm-gateway-sdk
# or
yarn add @aisera/llm-gateway-sdk
```

#### Basic Usage

```javascript
import { LLMGatewayClient } from '@aisera/llm-gateway-sdk';

// Initialize the client
const client = new LLMGatewayClient({
  apiKey: 'YOUR_API_KEY',
  tenantId: 'YOUR_TENANT_ID'
});

// Execute a prompt
async function executePrompt() {
  try {
    const response = await client.executePrompt({
      prompt: 'Explain quantum computing in simple terms',
      model: 'gpt-4'
    });
    
    console.log(response.text);
  } catch (error) {
    console.error('Error executing prompt:', error);
  }
}

executePrompt();

// Create a new prompt template
async function createPrompt() {
  try {
    const newPrompt = await client.createPrompt({
      name: 'Customer Service Response',
      description: 'Generate customer service responses for various scenarios',
      template: 'Please provide a professional customer service response to the following inquiry: {{inquiry}}',
      parameters: {
        inquiry: {
          type: 'string',
          description: 'The customer inquiry to respond to',
          required: true
        }
      }
    });
    
    console.log(`Created prompt with ID: ${newPrompt.id}`);
  } catch (error) {
    console.error('Error creating prompt:', error);
  }
}

createPrompt();
```

#### TypeScript Support

The SDK includes full TypeScript definitions:

```typescript
import { LLMGatewayClient, PromptExecutionParams, Prompt } from '@aisera/llm-gateway-sdk';

async function executeCustomPrompt(inquiry: string): Promise<string> {
  const client = new LLMGatewayClient({
    apiKey: 'YOUR_API_KEY',
    tenantId: 'YOUR_TENANT_ID'
  });
  
  const params: PromptExecutionParams = {
    promptId: 'pr_123456',
    parameters: {
      inquiry
    },
    model: 'claude-3-opus'
  };
  
  const response = await client.executePromptById(params);
  return response.text;
}
```

### Java SDK

Java SDK documentation is available at [https://docs.aisera.com/llm-gateway/sdk/java](https://docs.aisera.com/llm-gateway/sdk/java).

### Other Languages

Community-maintained libraries for other languages:

- [Go SDK](https://github.com/aisera-community/llm-gateway-go)
- [Ruby SDK](https://github.com/aisera-community/llm-gateway-ruby)
- [.NET SDK](https://github.com/aisera-community/llm-gateway-dotnet)

## Code Samples

The following code samples demonstrate common integration patterns.

### Chat Interface Integration

```javascript
// React/Next.js example - Chat interface
import { useState } from 'react';
import { LLMGatewayClient } from '@aisera/llm-gateway-sdk';

const client = new LLMGatewayClient({
  apiKey: process.env.AISERA_API_KEY,
  tenantId: process.env.AISERA_TENANT_ID
});

export default function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  async function handleSubmit(e) {
    e.preventDefault();
    if (!input.trim()) return;
    
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      const response = await client.executeChatPrompt({
        messages: [...messages, userMessage].map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        model: 'gpt-4'
      });
      
      setMessages(prev => [
        ...prev, 
        { role: 'assistant', content: response.text }
      ]);
    } catch (error) {
      console.error('Error in chat:', error);
      setMessages(prev => [
        ...prev, 
        { 
          role: 'system', 
          content: 'Sorry, there was an error processing your request.'
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  }
  
  return (
    <div className="chat-container">
      <div className="message-list">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {isLoading && <div className="loading">AI is thinking...</div>}
      </div>
      
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}
```

### Stream Response Processing

```python
from aisera.llm_gateway import LLMGatewayClient

client = LLMGatewayClient(
    api_key="YOUR_API_KEY",
    tenant_id="YOUR_TENANT_ID"
)

# Stream a response in real-time
for chunk in client.execute_prompt_stream(
    prompt="Write a short story about a robot learning to paint",
    model="claude-3-opus",
    max_tokens=1000
):
    print(chunk.text, end="", flush=True)
```

### Batch Processing

```python
import csv
from concurrent.futures import ThreadPoolExecutor
from aisera.llm_gateway import LLMGatewayClient

client = LLMGatewayClient(
    api_key="YOUR_API_KEY",
    tenant_id="YOUR_TENANT_ID"
)

# Process a CSV file with customer questions
def process_customer_question(row):
    try:
        response = client.execute_prompt_by_id(
            prompt_id="pr_customer_service",
            parameters={
                "customer_name": row["Name"],
                "product": row["Product"],
                "question": row["Question"]
            }
        )
        return {
            "customer_id": row["ID"],
            "question": row["Question"],
            "answer": response.text
        }
    except Exception as e:
        print(f"Error processing {row['ID']}: {str(e)}")
        return {
            "customer_id": row["ID"],
            "question": row["Question"],
            "answer": "Error: " + str(e)
        }

# Read questions from CSV
with open("customer_questions.csv", "r") as f:
    reader = csv.DictReader(f)
    questions = list(reader)

# Process in parallel with appropriate rate limiting
results = []
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(process_customer_question, row) for row in questions]
    for future in futures:
        result = future.result()
        results.append(result)

# Write results to CSV
with open("customer_answers.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["customer_id", "question", "answer"])
    writer.writeheader()
    writer.writerows(results)
```

## Tools & Utilities

### Command-Line Interface (CLI)

The LLM Gateway CLI provides command-line access to API functionality.

#### Installation

```bash
npm install -g @aisera/llm-gateway-cli
```

#### Usage

```bash
# Configure credentials
llm-gateway config set api-key YOUR_API_KEY
llm-gateway config set tenant-id YOUR_TENANT_ID

# Execute a prompt
llm-gateway execute "Explain the concept of recursion"

# Execute with a specific model
llm-gateway execute "Explain the concept of recursion" --model gpt-4

# List available LLM models
llm-gateway models list

# Create a new prompt from a template file
llm-gateway prompts create --file ./my-prompt-template.json

# Test a prompt template with parameters
llm-gateway prompts test pr_123456 --params '{"topic":"AI","question":"How does it work?"}'

# Export all prompts to a directory
llm-gateway prompts export --dir ./prompts-backup

# Import prompts from a directory
llm-gateway prompts import --dir ./prompts-backup
```

### Postman Collection

A complete [Postman](https://www.postman.com/) collection is available for testing the API:

1. Download the collection: [LLM Gateway API.postman_collection.json](https://api.aisera.com/resources/LLM_Gateway_API.postman_collection.json)
2. Import into Postman
3. Configure environment variables for `api_key` and `tenant_id`

### VS Code Extension

The LLM Gateway VS Code extension provides IDE integration for prompt development.

Features:
- Syntax highlighting for prompt templates
- Parameter validation
- Direct prompt testing from the editor
- Version management
- Template snippets

Install from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=Aisera.llm-gateway)

## Client Libraries

These libraries provide more specialized functionality on top of the core SDKs.

### Prompt Library Manager

A tool for managing prompt templates as code:

```bash
npm install @aisera/prompt-manager
```

```javascript
import { PromptManager } from '@aisera/prompt-manager';

// Initialize
const manager = new PromptManager({
  sourceDir: './prompts',
  apiKey: 'YOUR_API_KEY',
  tenantId: 'YOUR_TENANT_ID'
});

// Sync local prompt templates with the API
async function syncPrompts() {
  // This will create/update prompts in the API based on your local files
  const results = await manager.syncAll();
  
  console.log(`Synced ${results.length} prompts:`);
  for (const result of results) {
    console.log(`${result.name}: ${result.status}`);
  }
}

syncPrompts();
```

### Data Extraction Toolkit

A toolkit for extracting structured data from text using the LLM Gateway:

```bash
pip install aisera-llm-extraction
```

```python
from aisera.llm_extraction import Extractor

extractor = Extractor(
    api_key="YOUR_API_KEY",
    tenant_id="YOUR_TENANT_ID",
    model="claude-3-opus"
)

# Define a schema for extraction
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "phone": {"type": "string"},
        "request_type": {"type": "string", "enum": ["support", "sales", "billing", "other"]},
        "priority": {"type": "string", "enum": ["low", "medium", "high"]},
        "description": {"type": "string"}
    },
    "required": ["name", "email", "request_type", "description"]
}

# Extract structured data from text
text = """
Hello,

My name is John Smith and I'm having trouble accessing my account. 
I've been trying to log in for the past 2 days with no success.
This is preventing me from completing an important project due tomorrow.

You can reach me at john.smith@example.com or 555-123-4567.

Thanks,
John
"""

result = extractor.extract(text, schema)
print(result)
# Output:
# {
#   'name': 'John Smith',
#   'email': 'john.smith@example.com',
#   'phone': '555-123-4567',
#   'request_type': 'support',
#   'priority': 'high',
#   'description': 'Having trouble accessing account, unable to log in for 2 days, preventing completion of important project due tomorrow'
# }
```

## Community Resources

### GitHub Repositories

- [LLM Gateway Examples](https://github.com/aisera/llm-gateway-examples): Collection of examples and integrations
- [LLM Gateway Community](https://github.com/aisera-community): Community-maintained tools and resources

### Community Projects

- [Streamlit Integration](https://github.com/aisera-community/streamlit-llm-gateway): Streamlit components for LLM Gateway
- [Laravel Package](https://github.com/aisera-community/laravel-llm-gateway): Laravel integration package
- [Django Integration](https://github.com/aisera-community/django-llm-gateway): Django integration app

### Forums and Support

- [Community Discord](https://discord.gg/aisera-llm-gateway)
- [Stack Overflow Tag](https://stackoverflow.com/questions/tagged/llm-gateway)
- [GitHub Discussions](https://github.com/aisera/llm-gateway-examples/discussions)