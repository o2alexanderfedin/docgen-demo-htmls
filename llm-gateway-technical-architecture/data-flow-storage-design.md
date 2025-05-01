# Data Flow and Storage Design

## Table of Contents

- [Introduction](#introduction)
- [Data Models](#data-models)
  - [Core Domain Entities](#core-domain-entities)
  - [Request/Response Objects](#requestresponse-objects)
  - [Configuration Models](#configuration-models)
- [Storage Architecture](#storage-architecture)
  - [Database Schema](#database-schema)
  - [Cache Architecture](#cache-architecture)
- [Data Flows](#data-flows)
  - [Prompt Execution Flow](#prompt-execution-flow)
  - [Prompt Management Flow](#prompt-management-flow)
  - [Analytics Collection Flow](#analytics-collection-flow)
- [Data Serialization](#data-serialization)
- [Data Retention and Lifecycle](#data-retention-and-lifecycle)

## Introduction

This document details the data flow and storage architecture of the LLM Gateway, including entity models, database schemas, caching strategies, and the lifecycle of data as it moves through the system. The LLM Gateway handles various types of data including user requests, LLM responses, prompt templates, configuration settings, and analytics information.

## Data Models

### Core Domain Entities

The core domain entities represent the primary data structures that are persisted in the system's storage.

```mermaid
classDiagram
    class LLMPromptRegistryEntity {
        <<entity>>
        +id: String
        +name: String
        +description: String
        +template: String
        +createdBy: String
        +createdAt: Timestamp
        +updatedAt: Timestamp
        +status: String
        +tenantId: String
        +tags: List~String~
    }
    
    class LLMPromptRegistryMappingEntity {
        <<entity>>
        +id: String
        +promptId: String
        +paramName: String
        +paramType: String
        +description: String
        +required: Boolean
        +defaultValue: String
    }
    
    class LLMPromptVersioningEntity {
        <<entity>>
        +id: String
        +promptId: String
        +version: String
        +template: String
        +createdBy: String
        +createdAt: Timestamp
        +status: String
        +comments: String
    }
    
    class LLMRegistryEntity {
        <<entity>>
        +id: String
        +name: String
        +description: String
        +provider: String
        +modelId: String
        +defaultParams: Map~String, Object~
        +createdAt: Timestamp
        +updatedAt: Timestamp
        +status: String
    }
    
    LLMPromptRegistryEntity "1" -- "many" LLMPromptRegistryMappingEntity : contains
    LLMPromptRegistryEntity "1" -- "many" LLMPromptVersioningEntity : has versions
```

**Entity Descriptions:**

- `LLMPromptRegistryEntity`: Represents a prompt template with metadata
- `LLMPromptRegistryMappingEntity`: Defines parameters for prompt templates
- `LLMPromptVersioningEntity`: Tracks versions of prompt templates
- `LLMRegistryEntity`: Describes available LLM models and configurations

### Request/Response Objects

These data structures represent the request and response objects used in API interactions.

```mermaid
classDiagram
    class LLMFetchAnswerRequestDTO {
        <<dto>>
        +prompt: String
        +maxTokens: Integer
        +temperature: Float
        +provider: String
        +model: String
        +options: Map~String, Object~
    }
    
    class LLMFetchAnswerResponseDTO {
        <<dto>>
        +response: String
        +provider: String
        +model: String
        +usageMetrics: Map~String, Object~
        +tokenCount: Integer
        +completionId: String
    }
    
    class LLMFetchChatAnswerRequestDTO {
        <<dto>>
        +messages: List~ChatMessageDTO~
        +maxTokens: Integer
        +temperature: Float
        +provider: String
        +model: String
        +options: Map~String, Object~
        +functionDefinitions: List~FunctionDefinition~
    }
    
    class LLMFetchChatAnswerResponseDTO {
        <<dto>>
        +message: ChatMessageDTO
        +provider: String
        +model: String
        +usageMetrics: Map~String, Object~
        +tokenCount: Integer
        +completionId: String
        +functionCall: FunctionCallDTO
    }
    
    class ChatMessageDTO {
        <<dto>>
        +role: String
        +content: String
    }
    
    class FunctionDefinition {
        <<dto>>
        +name: String
        +description: String
        +parameters: FunctionParameters
    }
    
    class FunctionCallDTO {
        <<dto>>
        +name: String
        +arguments: String
    }
    
    LLMFetchChatAnswerRequestDTO --> ChatMessageDTO : contains
    LLMFetchChatAnswerRequestDTO --> FunctionDefinition : defines
    LLMFetchChatAnswerResponseDTO --> ChatMessageDTO : returns
    LLMFetchChatAnswerResponseDTO --> FunctionCallDTO : may include
    FunctionDefinition --> FunctionParameters : defines
```

**DTO Descriptions:**

- `LLMFetchAnswerRequestDTO`: Request for basic text completion
- `LLMFetchAnswerResponseDTO`: Response from text completion
- `LLMFetchChatAnswerRequestDTO`: Request for chat-based completion
- `LLMFetchChatAnswerResponseDTO`: Response from chat-based completion
- `ChatMessageDTO`: Represents a message in a chat conversation
- `FunctionDefinition`: Defines a function that can be called by the LLM
- `FunctionCallDTO`: Represents a function call in an LLM response

### Configuration Models

These models represent configuration settings for the system.

```mermaid
classDiagram
    class LLMCacheTenantConfig {
        <<config>>
        +enabled: Boolean
        +defaultTTL: Duration
        +maxEntries: Integer
        +allowedNamespaces: Set~String~
    }
    
    class ClientRequestConfigs {
        <<config>>
        +timeout: Duration
        +retryCount: Integer
        +retryBackoff: Duration
        +maxConcurrentRequests: Integer
        +rateLimitPerMinute: Integer
    }
```

**Configuration Descriptions:**

- `LLMCacheTenantConfig`: Tenant-specific cache configuration
- `ClientRequestConfigs`: Configuration for LLM client requests including timeouts and retries

## Storage Architecture

The LLM Gateway uses multiple storage systems for different types of data:

1. **Relational Database**: For structured data like prompt templates and configurations
2. **Redis Cache**: For high-speed access to frequently used data and LLM responses
3. **Time-Series Database**: For metrics and analytics data
4. **Log Storage**: For audit logs and operational logs

### Database Schema

The primary database schema includes the following tables:

```mermaid
erDiagram
    LLM_PROMPT_REGISTRY {
        varchar id PK
        varchar name
        text description
        text template
        varchar created_by
        timestamp created_at
        timestamp updated_at
        varchar status
        varchar tenant_id
        varchar[] tags
    }
    
    LLM_PROMPT_REGISTRY_MAPPING {
        varchar id PK
        varchar prompt_id FK
        varchar param_name
        varchar param_type
        text description
        boolean required
        text default_value
    }
    
    LLM_PROMPT_VERSIONING {
        varchar id PK
        varchar prompt_id FK
        varchar version
        text template
        varchar created_by
        timestamp created_at
        varchar status
        text comments
    }
    
    LLM_REGISTRY {
        varchar id PK
        varchar name
        text description
        varchar provider
        varchar model_id
        jsonb default_params
        timestamp created_at
        timestamp updated_at
        varchar status
    }
    
    TENANT_CONFIG {
        varchar tenant_id PK
        jsonb cache_config
        jsonb client_config
        jsonb analytics_config
        timestamp updated_at
    }
    
    LLM_PROMPT_REGISTRY ||--o{ LLM_PROMPT_REGISTRY_MAPPING : "has parameters"
    LLM_PROMPT_REGISTRY ||--o{ LLM_PROMPT_VERSIONING : "has versions"
```

**Table Descriptions:**

- `LLM_PROMPT_REGISTRY`: Stores prompt templates and metadata
- `LLM_PROMPT_REGISTRY_MAPPING`: Maps parameters to prompt templates
- `LLM_PROMPT_VERSIONING`: Tracks versions of prompt templates
- `LLM_REGISTRY`: Stores information about available LLM models
- `TENANT_CONFIG`: Stores tenant-specific configuration settings

### Cache Architecture

The LLM Gateway uses a Redis-based cache for various caching needs:

```mermaid
graph TD
    subgraph "Redis Cache"
        Response["Response Cache<br>(Hash: Request → Response)"]
        TokenCount["Token Count Cache<br>(String: Text → Count)"]
        PromptCache["Prompt Template Cache<br>(Hash: ID → Template)"]
        ConfigCache["Config Cache<br>(Hash: TenantID → Config)"]
    end
    
    Client[Client] --> Gateway[LLM Gateway]
    Gateway --> CacheCheck{Cache Check}
    
    CacheCheck -->|Hit| Response
    Response -->|Return| Gateway
    
    CacheCheck -->|Miss| LLMProvider[LLM Provider]
    LLMProvider -->|Store| Response
    
    Gateway -->|Lookup| PromptCache
    Gateway -->|Lookup| ConfigCache
    Gateway -->|Count| TokenCount
```

**Cache Structures:**

1. **Response Cache**
   - Key: Hash of normalized request parameters
   - Value: Serialized response object
   - TTL: Configurable per tenant and request type
   - Eviction: LRU when memory limit reached

2. **Token Count Cache**
   - Key: Hash of text content
   - Value: Token count
   - TTL: Long-lived (days)
   - Purpose: Optimize token counting for repeated content

3. **Prompt Template Cache**
   - Key: Prompt template ID
   - Value: Compiled template with parameter definitions
   - Invalidation: On template updates
   - Purpose: Speed up prompt rendering

4. **Configuration Cache**
   - Key: Tenant ID
   - Value: Serialized configuration objects
   - Invalidation: On configuration changes
   - Purpose: Reduce database load for config lookups

## Data Flows

### Prompt Execution Flow

This flow illustrates how data moves through the system during prompt execution:

```mermaid
flowchart TD
    Client[Client] -->|1. Submit Request| API[API Layer]
    
    API -->|2. Authenticate| Auth[Auth Service]
    Auth -->|Result| API
    
    API -->|3. Validate| Validator[Request Validator]
    Validator -->|Result| API
    
    API -->|4. Get Prompt| PromptMgr[Prompt Manager]
    PromptMgr -->|4.1 Check Cache| PromptCache[(Prompt Cache)]
    PromptCache -->|4.2 Return or Load| PromptMgr
    PromptMgr -->|4.3 Render| API
    
    API -->|5. Execute| ExecMgr[Execution Manager]
    
    ExecMgr -->|5.1 Check Cache| ResponseCache[(Response Cache)]
    ResponseCache -->|5.2 Cache Hit?| ExecMgr
    
    ExecMgr -->|5.3a Cache Miss| ClientMgr[Client Manager]
    ClientMgr -->|5.4 Select Provider| Providers[LLM Provider]
    Providers -->|5.5 Return Response| ClientMgr
    ClientMgr -->|5.6 Process Response| ExecMgr
    
    ExecMgr -->|5.7 Store in Cache| ResponseCache
    ExecMgr -->|5.8 Record Analytics| Analytics[Analytics Service]
    ExecMgr -->|5.9 Audit| AuditLog[(Audit Log)]
    
    ExecMgr -->|5.10 Return Response| API
    API -->|6. Format & Return| Client
```

**Data Flow Description:**

1. Client submits a request with prompt parameters
2. API layer authenticates the request
3. Request is validated for correctness
4. If prompt ID provided, template is retrieved and rendered
5. Execution manager checks cache for identical request
6. If cache miss, appropriate client is selected and called
7. Response is processed, cached, and analytics are recorded
8. Formatted response is returned to client

### Prompt Management Flow

This flow illustrates the data flow for prompt template management:

```mermaid
flowchart TD
    Client[Client] -->|1. Submit Template| API[API Layer]
    
    API -->|2. Authenticate| Auth[Auth Service]
    Auth -->|Result| API
    
    API -->|3. Validate| Validator[Request Validator]
    Validator -->|Result| API
    
    API -->|4. Process Request| PromptMgr[Prompt Manager]
    
    subgraph "Prompt Creation Flow"
        PromptMgr -->|4.1 Create Template| DB[(Database)]
        PromptMgr -->|4.2 Extract Params| ParamExtractor[Parameter Extractor]
        ParamExtractor -->|4.3 Param Definitions| PromptMgr
        PromptMgr -->|4.4 Store Params| DB
    end
    
    subgraph "Version Management Flow"
        PromptMgr -->|4.5 Create Version| DB
        PromptMgr -->|4.6 Update Status| DB
    end
    
    PromptMgr -->|4.7 Invalidate Cache| PromptCache[(Prompt Cache)]
    PromptMgr -->|4.8 Audit Change| AuditLog[(Audit Log)]
    
    PromptMgr -->|4.9 Return Result| API
    API -->|5. Format & Return| Client
```

**Data Flow Description:**

1. Client submits a prompt template creation/update request
2. API layer authenticates the request
3. Template is validated for correctness and syntax
4. Prompt manager processes the template
5. Parameters are extracted and stored
6. Version information is created if applicable
7. Cache is invalidated for the affected template
8. Audit record is created for the change
9. Result is returned to the client

### Analytics Collection Flow

This flow illustrates how analytics data is collected and processed:

```mermaid
flowchart TD
    ExecMgr[Execution Manager] -->|1. Record Usage| Analytics[Analytics Handler]
    
    Analytics -->|2.1 Extract Metrics| MetricProcessor[Metric Processor]
    MetricProcessor -->|2.2 Format Metrics| Analytics
    
    Analytics -->|3.1 Store Real-time| RTMetrics[(Real-time Metrics)]
    Analytics -->|3.2 Buffer for Batch| Buffer[Metrics Buffer]
    
    Buffer -->|4. Batch Process| BatchProcessor[Batch Processor]
    BatchProcessor -->|5. Store Historical| TSDB[(Time Series DB)]
    
    Dashboard[Analytics Dashboard] -->|6. Query| TSDB
    Dashboard -->|7. Query| RTMetrics
```

**Data Flow Description:**

1. Execution manager records usage after each request
2. Analytics handler extracts and formats metrics
3. Real-time metrics are stored for immediate access
4. Metrics are buffered for batch processing
5. Batch processor aggregates and stores historical metrics
6. Analytics dashboards query both real-time and historical data

## Data Serialization

The LLM Gateway uses the following serialization strategies:

1. **JSON Serialization**
   - Used for API requests/responses
   - Used for cache storage
   - Library: Jackson with custom serializers/deserializers

2. **Protocol Buffers**
   - Used for gRPC interfaces
   - Used for some high-volume internal communication
   - Provides more compact binary representation

3. **Database Mapping**
   - ORM: Hibernate for entity-relational mapping
   - Custom converters for complex types
   - JSON column types for flexible schema

## Data Retention and Lifecycle

The LLM Gateway implements the following data retention policies:

1. **Prompt Templates**
   - Retention: Indefinite (with soft deletion option)
   - Versioning: All versions retained by default
   - Archive Policy: Manual archiving of unused templates

2. **Cache Data**
   - LLM Response Cache: TTL-based expiration (minutes to hours)
   - Token Count Cache: TTL-based expiration (days)
   - Eviction: LRU algorithm when memory limits reached

3. **Analytics Data**
   - Raw Metrics: 7-30 days (configurable)
   - Aggregated Metrics: 1 year+
   - Rollup Strategy: Hourly → Daily → Monthly aggregation

4. **Audit Logs**
   - Security Events: 1 year minimum
   - Operational Events: 90 days
   - Retention Policy: Configurable per tenant and log type

---

**Previous**: [Module-Level Architecture](./module-level-architecture.md) | **Next**: [Runtime Behavior & Concurrency](./runtime-behavior-concurrency.md)