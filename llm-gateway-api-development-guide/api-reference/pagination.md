# Pagination, Filtering, and Sorting

This guide explains how to work with large collections of data in the LLM Gateway API, covering pagination mechanisms, filtering options, and sorting capabilities.

## Table of Contents

- [Pagination](#pagination)
- [Filtering](#filtering)
- [Sorting](#sorting)
- [Examples](#examples)

## Pagination

All endpoints that return collections of resources support pagination to limit the number of items returned in a single response and to navigate through large result sets efficiently.

### Pagination Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | The page number to retrieve |
| limit | integer | 20 | The number of items per page (maximum 100) |

### Pagination Response

Paginated responses include a `pagination` object containing metadata about the result set:

```json
{
  "items": [...],
  "pagination": {
    "total": 45,     // Total number of items available
    "limit": 20,     // Number of items per page
    "page": 1,       // Current page number
    "pages": 3       // Total number of pages
  }
}
```

### Pagination Headers

In addition to the response body, the following pagination headers are included:

| Header | Description |
|--------|-------------|
| X-Total-Count | The total number of items available |
| X-Page-Count | The total number of pages available |
| X-Page | The current page number |
| X-Limit | The number of items per page |

## Filtering

Most collection endpoints support filtering to narrow down the results based on specific criteria.

### Common Filter Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| status | string | Filter by resource status | `status=published` |
| name | string | Filter by resource name (substring match) | `name=customer` |
| created_after | ISO date | Filter by creation date | `created_after=2023-01-01T00:00:00Z` |
| created_before | ISO date | Filter by creation date | `created_before=2023-12-31T23:59:59Z` |
| model | string | Filter by LLM model | `model=gpt-4` |
| provider | string | Filter by LLM provider | `provider=openai` |

### Filter Operators

The API supports several operators for more complex filtering:

| Operator | Description | Example |
|----------|-------------|---------|
| eq | Equals | `status.eq=published` |
| ne | Not equals | `status.ne=draft` |
| gt | Greater than | `version.gt=3` |
| gte | Greater than or equal | `version.gte=3` |
| lt | Less than | `version.lt=10` |
| lte | Less than or equal | `version.lte=10` |
| in | In a list | `status.in=published,archived` |
| like | Pattern matching | `name.like=%customer%` |

### Combining Filters

Multiple filters can be combined to create advanced queries. All applied filters are combined with a logical AND operation.

## Sorting

Collection endpoints support sorting to order the results based on specific fields.

### Sort Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| sort | string | Field to sort by | `sort=createdAt` |
| order | string | Sort order (asc or desc) | `order=desc` |

### Multiple Sort Fields

To sort by multiple fields, specify them as comma-separated values:

```
sort=status,createdAt&order=asc,desc
```

This sorts first by status (ascending) and then by createdAt (descending).

## Examples

### Basic Pagination

Retrieve the second page of prompts with 10 items per page:

```bash
curl "https://api.aisera.com/v1/tenants/9000/llm/prompts?page=2&limit=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Filtering by Status and Name

Retrieve all published prompts containing "customer" in their name:

```bash
curl "https://api.aisera.com/v1/tenants/9000/llm/prompts?status=published&name=customer" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Advanced Filtering

Retrieve prompts created between January and June 2023, with version greater than or equal to 2:

```bash
curl "https://api.aisera.com/v1/tenants/9000/llm/prompts?created_after=2023-01-01T00:00:00Z&created_before=2023-06-30T23:59:59Z&version.gte=2" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Sorting

Retrieve prompts sorted by creation date in descending order (newest first):

```bash
curl "https://api.aisera.com/v1/tenants/9000/llm/prompts?sort=createdAt&order=desc" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Combined Example

Retrieve the first page of 20 published prompts, sorted by name in ascending order:

```bash
curl "https://api.aisera.com/v1/tenants/9000/llm/prompts?status=published&sort=name&order=asc&page=1&limit=20" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Python Example

```python
import requests

api_key = "YOUR_API_KEY"
base_url = "https://api.aisera.com"
tenant_id = "9000"

# Get the second page of recently created prompts
params = {
    "page": 2,
    "limit": 15,
    "sort": "createdAt",
    "order": "desc",
    "status": "published"
}

response = requests.get(
    f"{base_url}/v1/tenants/{tenant_id}/llm/prompts",
    headers={
        "Authorization": f"Bearer {api_key}"
    },
    params=params
)

data = response.json()
print(f"Retrieved {len(data['items'])} items")
print(f"Page {data['pagination']['page']} of {data['pagination']['pages']}")
print(f"Total items: {data['pagination']['total']}")

# Process the items
for item in data['items']:
    print(f"Prompt: {item['name']} (ID: {item['id']})")
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const apiKey = 'YOUR_API_KEY';
const baseUrl = 'https://api.aisera.com';
const tenantId = '9000';

// Get prompts filtered by name and creation date
async function getFilteredPrompts() {
  try {
    const response = await axios.get(
      `${baseUrl}/v1/tenants/${tenantId}/llm/prompts`,
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`
        },
        params: {
          'name.like': '%customer%',
          'created_after': '2023-01-01T00:00:00Z',
          'sort': 'name',
          'order': 'asc',
          'limit': 50
        }
      }
    );
    
    const { items, pagination } = response.data;
    console.log(`Retrieved ${items.length} items`);
    console.log(`Page ${pagination.page} of ${pagination.pages}`);
    console.log(`Total items: ${pagination.total}`);
    
    // Process the items
    items.forEach(item => {
      console.log(`Prompt: ${item.name} (ID: ${item.id})`);
    });
    
    // Check if there are more pages
    if (pagination.page < pagination.pages) {
      console.log('More pages available. Increase the page parameter to retrieve more items.');
    }
  } catch (error) {
    console.error('Error retrieving prompts:', error.message);
  }
}

getFilteredPrompts();
```