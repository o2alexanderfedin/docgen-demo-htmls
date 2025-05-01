# Authentication & Authorization

This guide explains how to authenticate with the LLM Gateway API and manage authorization for your requests.

## Table of Contents

- [Authentication Methods](#authentication-methods)
  - [API Key Authentication](#api-key-authentication)
  - [Bearer Token Authentication](#bearer-token-authentication)
  - [OAuth 2.0](#oauth-20)
- [Obtaining Access Tokens](#obtaining-access-tokens)
  - [Creating API Keys](#creating-api-keys)
  - [Acquiring OAuth Tokens](#acquiring-oauth-tokens)
- [Using Tokens in Requests](#using-tokens-in-requests)
  - [Header-Based Authentication](#header-based-authentication)
  - [Query Parameter Authentication](#query-parameter-authentication)
- [Role-Based Access Control](#role-based-access-control)
- [Tenant Isolation](#tenant-isolation)
- [Security Best Practices](#security-best-practices)

## Authentication Methods

The LLM Gateway API supports multiple authentication methods to provide flexibility for different integration scenarios.

### API Key Authentication

API key authentication is the simplest method for accessing the LLM Gateway API. Each API key is associated with a specific tenant and has a set of permissions.

#### API Key Format

API keys are 32-character alphanumeric strings prefixed with `llm_` (e.g., `llm_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p`).

#### Using API Keys

When using API key authentication, include the key in the `X-API-Key` header:

```http
GET /llm/v1/prompt_group/list HTTP/1.1
Host: api.aisera.com
X-API-Key: llm_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

### Bearer Token Authentication

Bearer token authentication uses JWT (JSON Web Tokens) for authentication. This method is preferred for most production applications.

#### Bearer Token Format

Bearer tokens are JWTs issued by the Aisera authentication service. They contain information about the user, tenant, and permissions.

#### Using Bearer Tokens

Include the bearer token in the `Authorization` header with the `Bearer` prefix:

```http
GET /llm/v1/prompt_group/list HTTP/1.1
Host: api.aisera.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### OAuth 2.0

For applications that need to act on behalf of users or integrate with third-party services, the LLM Gateway API supports OAuth 2.0 authentication.

#### Supported Grant Types

- Authorization Code Grant
- Client Credentials Grant
- Refresh Token Grant

#### OAuth Endpoints

| Endpoint | URL | Description |
|----------|-----|-------------|
| Authorization | `https://auth.aisera.com/oauth/authorize` | Used for authorization code flow |
| Token | `https://auth.aisera.com/oauth/token` | Used to obtain access tokens |
| Revoke | `https://auth.aisera.com/oauth/revoke` | Used to revoke tokens |

## Obtaining Access Tokens

### Creating API Keys

API keys can be created in the Aisera Admin Portal:

1. Log in to the [Aisera Admin Portal](https://admin.aisera.com)
2. Navigate to Settings > API Keys
3. Click "Create New API Key"
4. Select the desired permissions and expiration
5. Click "Generate Key"
6. Copy the key immediately (it will only be shown once)

#### API Key Permissions

When creating an API key, you can select from the following permission sets:

| Permission Set | Description |
|----------------|-------------|
| Read Only | Can only read prompts and prompt groups |
| Execute Only | Can only execute prompts |
| Read & Execute | Can read and execute prompts |
| Full Access | Can create, read, update, delete, and execute prompts |

### Acquiring OAuth Tokens

#### Client Credentials Flow

For server-to-server authentication, use the client credentials flow:

```bash
curl -X POST https://auth.aisera.com/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&scope=llm:read llm:execute"
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "llm:read llm:execute"
}
```

#### Authorization Code Flow

For web applications that need to act on behalf of users:

1. Redirect users to the authorization endpoint:

```
https://auth.aisera.com/oauth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=llm:read llm:execute
```

2. After the user authorizes your application, they'll be redirected to your `redirect_uri` with an authorization code:

```
https://your-app.com/callback?code=AUTHORIZATION_CODE
```

3. Exchange the authorization code for an access token:

```bash
curl -X POST https://auth.aisera.com/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=AUTHORIZATION_CODE&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&redirect_uri=YOUR_REDIRECT_URI"
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "def5020017a6748...",
  "scope": "llm:read llm:execute"
}
```

## Using Tokens in Requests

### Header-Based Authentication

The preferred method for authenticating with the LLM Gateway API is to use HTTP headers.

#### API Key Header

```http
GET /llm/v1/prompt_group/list HTTP/1.1
Host: api.aisera.com
X-API-Key: llm_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

#### Bearer Token Header

```http
GET /llm/v1/prompt_group/list HTTP/1.1
Host: api.aisera.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Query Parameter Authentication

For situations where setting headers is difficult, you can also authenticate using query parameters. However, this method is less secure and should be avoided in production environments.

```
GET /llm/v1/prompt_group/list?api_key=llm_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p HTTP/1.1
Host: api.aisera.com
```

**Note**: Query parameter authentication is only supported for API keys, not bearer tokens.

## Role-Based Access Control

The LLM Gateway API uses role-based access control (RBAC) to determine what actions a user or application can perform.

### Available Roles

| Role | Description |
|------|-------------|
| ADMIN | Full access to all API endpoints |
| USER | Can execute prompts and read/edit own prompts |
| READONLY | Can only read data, no modifications allowed |

### Permissions

Each role has a set of permissions:

| Permission | ADMIN | USER | READONLY |
|------------|-------|------|----------|
| Prompt Management | ✅ | ✅* | ❌ |
| Prompt Execution | ✅ | ✅ | ✅ |
| LLM Registry Management | ✅ | ❌ | ❌ |
| Versioning | ✅ | ✅* | ❌ |

*USER role can only manage prompts they created

### Endpoint-Specific Permissions

Different API endpoints require different permissions. These are documented in the [API Reference](./api-reference/README.md) section for each endpoint.

## Tenant Isolation

The LLM Gateway API enforces tenant isolation to ensure that data is properly segregated between different tenants. Each request must specify the tenant ID, and authentication credentials are validated against this tenant ID to ensure proper access.

### Tenant ID Specification

The tenant ID can be specified in one of two ways:

1. As a query parameter:
   ```
   GET /llm/v1/prompt_group/list?tenantId=9000 HTTP/1.1
   ```

2. In the request path (for tenant-specific endpoints):
   ```
   GET /v1/tenants/9000/llm/prompts HTTP/1.1
   ```

### Default Tenant

If no tenant ID is specified, the default tenant ID (`9000`) is used. However, it's strongly recommended to explicitly specify the tenant ID in all requests.

## Security Best Practices

### Token Security

- Never store API keys or bearer tokens in client-side code
- Use environment variables or secure key management services to store tokens
- Rotate API keys regularly
- Use the principle of least privilege (only grant necessary permissions)

### Transport Security

- Always use HTTPS when communicating with the LLM Gateway API
- Validate SSL/TLS certificates
- Use secure cipher suites

### Token Expiration and Refresh

Bearer tokens have an expiration time (typically 1 hour). Monitor the expiration and refresh tokens as needed:

#### Checking Token Expiration

Decode the JWT to check its expiration time:

```javascript
// JavaScript example
function isTokenExpired(token) {
  const payload = JSON.parse(atob(token.split('.')[1]));
  return payload.exp * 1000 < Date.now();
}
```

#### Refreshing Tokens

Use the refresh token to obtain a new access token:

```bash
curl -X POST https://auth.aisera.com/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token&refresh_token=REFRESH_TOKEN&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET"
```

### Revoking Tokens

If a token is compromised, revoke it immediately:

```bash
curl -X POST https://auth.aisera.com/oauth/revoke \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "token=ACCESS_TOKEN&token_type_hint=access_token&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET"
```