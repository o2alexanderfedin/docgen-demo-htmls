# Domain Model and Business Logic

## Table of Contents

- [Introduction](#introduction)
- [Core Domain Concepts](#core-domain-concepts)
- [Domain Model](#domain-model)
  - [LLM Domain](#llm-domain)
  - [Prompt Domain](#prompt-domain)
  - [Execution Domain](#execution-domain)
  - [Analytics Domain](#analytics-domain)
- [Service Layer](#service-layer)
  - [Service Interactions](#service-interactions)
- [Business Logic](#business-logic)
  - [Prompt Management](#prompt-management)
  - [Execution Logic](#execution-logic)
  - [Provider Selection](#provider-selection)
  - [Caching Strategy](#caching-strategy)
- [Cross-Cutting Concerns](#cross-cutting-concerns)
  - [Multi-Tenancy](#multi-tenancy)
  - [Authorization and Access Control](#authorization-and-access-control)
  - [Auditing and Compliance](#auditing-and-compliance)
- [Domain Events](#domain-events)
- [Business Rules](#business-rules)

## Introduction

This document describes the domain model and business logic of the LLM Gateway. It explains the core domain concepts, entities, relationships, and the services that implement the business logic. The domain model provides a conceptual framework for understanding the system, while the business logic describes how these concepts interact to fulfill the system's requirements.

## Core Domain Concepts

The LLM Gateway's domain centers around several core concepts:

1. **LLM Provider**: An external service that provides large language model capabilities
2. **Prompt**: A template with variables that is rendered and sent to an LLM
3. **Execution**: The process of sending a prompt to an LLM and receiving a response
4. **Cache**: Storage for LLM responses to improve performance and reduce costs
5. **Tenant**: An organization or logical grouping of users and resources
6. **Metrics**: Usage and performance data for analysis and billing

These concepts form the foundation of the domain model and drive the system's architecture.

## Domain Model

### LLM Domain

The LLM domain encompasses the entities related to LLM providers and their capabilities:

```mermaid
classDiagram
    class LLMProvider {
        <<entity>>
        +String id
        +String name
        +String description
        +ProviderType type
        +List~ModelDefinition~ models
        +Map~String, Object~ defaultParameters
        +boolean supportsStreaming
        +boolean supportsChat
        +boolean supportsVision
        +int maxContextLength
    }
    
    class ModelDefinition {
        <<entity>>
        +String id
        +String name
        +String version
        +Map~String, Object~ capabilities
        +Map~String, Object~ limits
        +Map~String, Object~ pricing
    }
    
    class ProviderType {
        <<enumeration>>
        OPENAI
        ANTHROPIC
        BEDROCK
        AZURE_OPENAI
        CUSTOM
    }
    
    class ProviderCredentials {
        <<entity>>
        +String id
        +ProviderType type
        +String tenantId
        +Map~String, String~ credentials
        +boolean active
    }
    
    class ProviderConfig {
        <<entity>>
        +String id
        +ProviderType type
        +String tenantId
        +Map~String, Object~ configuration
        +int priority
        +boolean active
    }
    
    LLMProvider "1" -- "many" ModelDefinition : offers
    LLMProvider -- ProviderType : is of type
    ProviderType -- ProviderCredentials : requires
    ProviderType -- ProviderConfig : configured by
```

**Domain Logic:**

- `LLMProvider` entities represent available language model providers
- Each provider offers multiple `ModelDefinition` entities with specific capabilities
- `ProviderCredentials` store authentication information for providers
- `ProviderConfig` contains tenant-specific configuration for providers

### Prompt Domain

The Prompt domain encompasses the entities related to prompt templates and their parameters:

```mermaid
classDiagram
    class PromptTemplate {
        <<entity>>
        +String id
        +String name
        +String description
        +String template
        +String tenantId
        +List~PromptParameter~ parameters
        +String createdBy
        +Date createdAt
        +Date updatedAt
        +PromptStatus status
        +List~String~ tags
    }
    
    class PromptParameter {
        <<entity>>
        +String id
        +String name
        +String description
        +ParameterType type
        +boolean required
        +Object defaultValue
        +Map~String, Object~ constraints
    }
    
    class PromptVersion {
        <<entity>>
        +String id
        +String promptId
        +String version
        +String template
        +List~PromptParameter~ parameters
        +String createdBy
        +Date createdAt
        +PromptStatus status
        +String comments
    }
    
    class ParameterType {
        <<enumeration>>
        STRING
        NUMBER
        BOOLEAN
        ARRAY
        OBJECT
        FUNCTION
    }
    
    class PromptStatus {
        <<enumeration>>
        DRAFT
        PUBLISHED
        ARCHIVED
        DEPRECATED
    }
    
    PromptTemplate "1" -- "many" PromptParameter : defines
    PromptTemplate "1" -- "many" PromptVersion : has
    PromptParameter -- ParameterType : is of type
    PromptTemplate -- PromptStatus : has status
    PromptVersion -- PromptStatus : has status
```

**Domain Logic:**

- `PromptTemplate` entities represent prompt templates with variables
- Each template defines `PromptParameter` entities that specify expected inputs
- `PromptVersion` entities track changes to templates over time
- Templates can be in different states represented by `PromptStatus`

### Execution Domain

The Execution domain encompasses the entities related to executing prompts and handling responses:

```mermaid
classDiagram
    class LLMRequest {
        <<entity>>
        +String id
        +String tenantId
        +RequestType type
        +Optional~String~ promptId
        +Map~String, Object~ parameters
        +String providerType
        +String modelId
        +Map~String, Object~ providerOptions
        +ExecutionOptions options
        +Date timestamp
    }
    
    class LLMResponse {
        <<entity>>
        +String id
        +String requestId
        +String content
        +String providerType
        +String modelId
        +Map~String, Object~ usageMetrics
        +ResponseStatus status
        +Date timestamp
        +Optional~FunctionCall~ functionCall
    }
    
    class ExecutionOptions {
        <<value object>>
        +int maxTokens
        +float temperature
        +boolean stream
        +int timeout
        +boolean cache
        +int cacheTTL
    }
    
    class RequestType {
        <<enumeration>>
        TEXT_COMPLETION
        CHAT_COMPLETION
    }
    
    class ResponseStatus {
        <<enumeration>>
        SUCCESS
        ERROR
        TIMEOUT
        CANCELLED
    }
    
    class FunctionCall {
        <<entity>>
        +String name
        +String arguments
    }
    
    class ExecutionContext {
        <<entity>>
        +String id
        +LLMRequest request
        +Optional~LLMResponse~ response
        +String tenantId
        +String userId
        +Map~String, Object~ metadata
        +Date startTime
        +Optional~Date~ endTime
        +ExecutionStatus status
    }
    
    class ExecutionStatus {
        <<enumeration>>
        PENDING
        EXECUTING
        COMPLETED
        FAILED
        CANCELLED
    }
    
    LLMRequest -- RequestType : is of type
    LLMRequest -- ExecutionOptions : configured by
    LLMResponse -- ResponseStatus : has status
    LLMResponse -- FunctionCall : may include
    ExecutionContext -- LLMRequest : contains
    ExecutionContext -- LLMResponse : contains
    ExecutionContext -- ExecutionStatus : has status
```

**Domain Logic:**

- `LLMRequest` entities represent requests to LLM providers
- `LLMResponse` entities represent responses from LLM providers
- `ExecutionContext` entities track the lifecycle of request execution
- `ExecutionOptions` define how requests should be processed

### Analytics Domain

The Analytics domain encompasses the entities related to usage metrics and analysis:

```mermaid
classDiagram
    class UsageRecord {
        <<entity>>
        +String id
        +String tenantId
        +String userId
        +String requestId
        +UsageType type
        +String providerType
        +String modelId
        +long tokenCount
        +Map~String, Object~ metrics
        +double cost
        +Date timestamp
    }
    
    class UsageType {
        <<enumeration>>
        PROMPT
        COMPLETION
        EMBEDDING
        FUNCTION_CALL
    }
    
    class UsageAggregate {
        <<entity>>
        +String id
        +String tenantId
        +AggregationPeriod period
        +Date startTime
        +Date endTime
        +Map~String, Object~ usageByProvider
        +Map~String, Object~ usageByModel
        +Map~String, Object~ usageByType
        +long totalTokens
        +double totalCost
    }
    
    class AggregationPeriod {
        <<enumeration>>
        HOURLY
        DAILY
        WEEKLY
        MONTHLY
    }
    
    class UsageLimit {
        <<entity>>
        +String id
        +String tenantId
        +LimitType type
        +String resourceId
        +long limit
        +LimitPeriod period
        +LimitAction action
    }
    
    class LimitType {
        <<enumeration>>
        TOKEN_COUNT
        REQUEST_COUNT
        COST
    }
    
    class LimitPeriod {
        <<enumeration>>
        DAILY
        WEEKLY
        MONTHLY
    }
    
    class LimitAction {
        <<enumeration>>
        ALERT
        THROTTLE
        BLOCK
    }
    
    UsageRecord -- UsageType : is of type
    UsageAggregate -- AggregationPeriod : for period
    UsageLimit -- LimitType : restricts
    UsageLimit -- LimitPeriod : over period
    UsageLimit -- LimitAction : triggers
```

**Domain Logic:**

- `UsageRecord` entities capture detailed usage information for each request
- `UsageAggregate` entities store aggregated usage statistics for reporting
- `UsageLimit` entities define usage constraints for tenants

## Service Layer

The Service Layer implements the business logic that operates on the domain model. The key services are:

```mermaid
classDiagram
    class PromptManager {
        <<service>>
        +getPrompt(id, version) PromptTemplate
        +listPrompts(filter) List~PromptTemplate~
        +createPrompt(template) PromptTemplate
        +updatePrompt(id, template) PromptTemplate
        +publishPrompt(id) PromptVersion
        +archivePrompt(id) void
        +renderPrompt(id, params) String
    }
    
    class ExecutionManager {
        <<service>>
        +execute(request) LLMResponse
        +streamExecute(request, handler) void
        +getExecutionContext(id) ExecutionContext
        +cancelExecution(id) boolean
    }
    
    class ProviderManager {
        <<service>>
        +getProvider(type) LLMProvider
        +listProviders() List~LLMProvider~
        +getProviderConfig(type, tenantId) ProviderConfig
        +updateProviderConfig(config) void
        +getCredentials(type, tenantId) ProviderCredentials
        +updateCredentials(credentials) void
    }
    
    class CacheManager {
        <<service>>
        +getCachedResponse(request) Optional~LLMResponse~
        +cacheResponse(request, response) void
        +invalidateCache(filter) void
        +getCacheStats() Map~String, Object~
    }
    
    class AnalyticsManager {
        <<service>>
        +recordUsage(record) void
        +getUsage(tenantId, filter) List~UsageRecord~
        +getAggregates(tenantId, period) UsageAggregate
        +checkLimit(tenantId, type) LimitStatus
    }
    
    class TenantManager {
        <<service>>
        +getTenantConfig(id) TenantConfig
        +updateTenantConfig(config) void
        +listTenants() List~TenantConfig~
        +validateTenant(id) boolean
    }
    
    PromptManager -- TenantManager : uses
    ExecutionManager -- PromptManager : uses
    ExecutionManager -- ProviderManager : uses
    ExecutionManager -- CacheManager : uses
    ExecutionManager -- AnalyticsManager : uses
    ExecutionManager -- TenantManager : uses
    ProviderManager -- TenantManager : uses
    CacheManager -- TenantManager : uses
    AnalyticsManager -- TenantManager : uses
```

### Service Interactions

The services interact to implement the system's business logic:

```mermaid
sequenceDiagram
    participant Client
    participant ExecMgr as ExecutionManager
    participant PromptMgr as PromptManager
    participant ProviderMgr as ProviderManager
    participant CacheMgr as CacheManager
    participant AnalyticsMgr as AnalyticsManager
    participant TenantMgr as TenantManager
    
    Client->>ExecMgr: execute(request)
    
    ExecMgr->>TenantMgr: validateTenant(tenantId)
    TenantMgr-->>ExecMgr: valid
    
    ExecMgr->>PromptMgr: renderPrompt(promptId, params)
    PromptMgr-->>ExecMgr: renderedPrompt
    
    ExecMgr->>CacheMgr: getCachedResponse(request)
    
    alt Cache Hit
        CacheMgr-->>ExecMgr: cachedResponse
    else Cache Miss
        CacheMgr-->>ExecMgr: empty
        
        ExecMgr->>ProviderMgr: getProvider(type)
        ProviderMgr-->>ExecMgr: provider
        
        ExecMgr->>ProviderMgr: getCredentials(type, tenantId)
        ProviderMgr-->>ExecMgr: credentials
        
        ExecMgr->>ExecMgr: callProvider(provider, credentials, request)
        
        ExecMgr->>CacheMgr: cacheResponse(request, response)
    end
    
    ExecMgr->>AnalyticsMgr: recordUsage(usageRecord)
    
    ExecMgr-->>Client: response
```

## Business Logic

### Prompt Management

The prompt management logic handles the lifecycle of prompt templates:

```mermaid
stateDiagram-v2
    [*] --> Draft
    
    state Draft {
        [*] --> Editing
        Editing --> Validating : Save Draft
        Validating --> SaveDraft : Valid
        Validating --> Editing : Invalid
        SaveDraft --> Editing : Continue Editing
        SaveDraft --> [*] : Complete Draft
    }
    
    Draft --> Publishing : Publish
    
    state Publishing {
        [*] --> Validating2
        Validating2 --> CreateVersion : Valid
        Validating2 --> [*] : Invalid
        CreateVersion --> UpdateStatus
        UpdateStatus --> [*]
    }
    
    Publishing --> Published : Success
    Publishing --> Draft : Failure
    
    Published --> Draft : Create New Draft
    Published --> Archiving : Archive
    
    state Archiving {
        [*] --> UpdateStatus2
        UpdateStatus2 --> [*]
    }
    
    Archiving --> Archived
    
    Archived --> [*]
```

**Key Business Rules:**

1. Prompt templates must have unique names within a tenant
2. Published templates cannot be modified directly - a new draft must be created
3. Templates must be syntactically valid before publishing
4. Template parameters must have defined types and validation rules
5. Draft templates can be modified by their creator or administrators
6. Published templates can be used by any authorized user within the tenant

### Execution Logic

The execution logic handles the processing of LLM requests:

```mermaid
flowchart TD
    Start([Start]) --> Validate{Validate\nRequest}
    
    Validate -->|Invalid| Error1[Return Error]
    Validate -->|Valid| Prompt{Prompt ID\nProvided?}
    
    Prompt -->|Yes| RenderPrompt[Render Prompt Template]
    Prompt -->|No| CheckCache[Check Response Cache]
    
    RenderPrompt --> CheckCache
    
    CheckCache --> CacheResult{Cache\nHit?}
    
    CacheResult -->|Yes| ReturnCached[Return Cached Response]
    
    CacheResult -->|No| SelectProvider[Select Provider]
    
    SelectProvider --> Provider{Provider\nAvailable?}
    
    Provider -->|No| Error2[Return Error]
    
    Provider -->|Yes| CheckLimit[Check Usage Limits]
    
    CheckLimit --> LimitResult{Limit\nExceeded?}
    
    LimitResult -->|Yes| Error3[Return Error]
    
    LimitResult -->|No| Stream{Streaming\nRequest?}
    
    Stream -->|Yes| StreamExecution[Stream Execution]
    Stream -->|No| SyncExecution[Synchronous Execution]
    
    StreamExecution --> RecordUsageStream[Record Usage]
    SyncExecution --> Cache[Cache Response]
    
    Cache --> RecordUsage[Record Usage]
    
    RecordUsage --> ReturnResponse[Return Response]
    RecordUsageStream --> End([End])
    
    ReturnCached --> End
    ReturnResponse --> End
    Error1 --> End
    Error2 --> End
    Error3 --> End
```

**Key Business Rules:**

1. Requests must be validated before execution
2. Tenant must be authenticated and authorized
3. If a prompt ID is provided, the template must be rendered
4. Cache should be checked before calling external providers
5. Provider selection follows priority and capability rules
6. Usage limits must be enforced before execution
7. Responses should be cached according to caching policy
8. Usage must be recorded for analytics and billing

### Provider Selection

The provider selection logic determines which LLM provider to use for a request:

```mermaid
flowchart TD
    Start([Start]) --> ExplicitProvider{Request\nSpecifies\nProvider?}
    
    ExplicitProvider -->|Yes| ValidateProvider{Provider\nValid?}
    ExplicitProvider -->|No| TenantDefault{Tenant\nDefault\nDefined?}
    
    ValidateProvider -->|Yes| CheckCapability{Provider\nSupports\nCapabilities?}
    ValidateProvider -->|No| Error1[Return Error]
    
    TenantDefault -->|Yes| UseDefault[Use Tenant Default]
    TenantDefault -->|No| SelectByCapability[Select Provider by Capability]
    
    UseDefault --> CheckCapability
    SelectByCapability --> CheckCapability
    
    CheckCapability -->|Yes| CheckAvailability{Provider\nAvailable?}
    CheckCapability -->|No| FallbackProvider{Fallback\nDefined?}
    
    FallbackProvider -->|Yes| UseFallback[Use Fallback Provider]
    FallbackProvider -->|No| Error2[Return Error]
    
    UseFallback --> CheckAvailability
    
    CheckAvailability -->|Yes| GetCredentials[Get Provider Credentials]
    CheckAvailability -->|No| Error3[Return Error]
    
    GetCredentials --> CreateClient[Create Provider Client]
    
    CreateClient --> End([End])
    
    Error1 --> End
    Error2 --> End
    Error3 --> End
```

**Key Business Rules:**

1. If the request explicitly specifies a provider, use it if valid
2. If no provider is specified, use tenant default if defined
3. Otherwise, select a provider based on required capabilities
4. Verify that the selected provider supports the required capabilities
5. Fall back to an alternative provider if defined and primary is unavailable
6. Provider must be available (not in failure state or circuit-broken)
7. Provider credentials must be available for the tenant

### Caching Strategy

The caching strategy determines if and how responses are cached:

```mermaid
flowchart TD
    Start([Start]) --> CachingEnabled{Caching\nEnabled?}
    
    CachingEnabled -->|Yes| RequestCacheable{Request\nCacheable?}
    CachingEnabled -->|No| SkipCache[Skip Cache]
    
    RequestCacheable -->|Yes| GenerateCacheKey[Generate Cache Key]
    RequestCacheable -->|No| SkipCache
    
    GenerateCacheKey --> CheckCache{Cache\nEntry\nExists?}
    
    CheckCache -->|Yes| ValidateEntry{Entry\nValid?}
    CheckCache -->|No| SkipCache
    
    ValidateEntry -->|Yes| ReturnCached[Return Cached Response]
    ValidateEntry -->|No| InvalidateEntry[Invalidate Entry]
    
    InvalidateEntry --> SkipCache
    
    SkipCache --> ExecuteRequest[Execute Request]
    
    ExecuteRequest --> ResponseCacheable{Response\nCacheable?}
    
    ResponseCacheable -->|Yes| CacheTTL{Cache\nTTL\nDefined?}
    ResponseCacheable -->|No| SkipCaching[Skip Caching]
    
    CacheTTL -->|Yes| UseDefined[Use Defined TTL]
    CacheTTL -->|No| UseDefault[Use Default TTL]
    
    UseDefined --> StoreCache[Store in Cache]
    UseDefault --> StoreCache
    
    StoreCache --> End([End])
    ReturnCached --> End
    SkipCaching --> End
```

**Key Business Rules:**

1. Caching must be enabled at system and tenant level
2. Request must be cacheable (deterministic, idempotent)
3. Cache key must uniquely identify the request
4. Cached entries must be validated before use
5. Invalid entries must be invalidated
6. Response must be cacheable (success, complete)
7. Cache TTL should respect request or default settings
8. Cache should respect tenant-specific storage limits

## Cross-Cutting Concerns

### Multi-Tenancy

The LLM Gateway implements a multi-tenant architecture:

```mermaid
graph TD
    subgraph "Tenant A"
        ConfigA[Configuration]
        PromptsA[Prompt Templates]
        CredentialsA[Provider Credentials]
        UsageA[Usage Metrics]
    end
    
    subgraph "Tenant B"
        ConfigB[Configuration]
        PromptsB[Prompt Templates]
        CredentialsB[Provider Credentials]
        UsageB[Usage Metrics]
    end
    
    subgraph "Tenant C"
        ConfigC[Configuration]
        PromptsC[Prompt Templates]
        CredentialsC[Provider Credentials]
        UsageC[Usage Metrics]
    end
    
    Gateway[LLM Gateway] --> TenantResolver[Tenant Resolver]
    
    TenantResolver --> ConfigA
    TenantResolver --> ConfigB
    TenantResolver --> ConfigC
    
    ConfigA --> IsolationA[Tenant Isolation]
    ConfigB --> IsolationB[Tenant Isolation]
    ConfigC --> IsolationC[Tenant Isolation]
    
    IsolationA --> ResourcesA[Resource Allocation]
    IsolationB --> ResourcesB[Resource Allocation]
    IsolationC --> ResourcesC[Resource Allocation]
```

**Multi-Tenancy Implementation:**

1. Tenant identification through API key, JWT, or request parameter
2. Tenant-specific configuration for providers, caching, limits
3. Data isolation at database and cache level
4. Resource allocation and throttling per tenant
5. Usage tracking and billing per tenant

### Authorization and Access Control

The LLM Gateway implements a role-based access control system:

```mermaid
graph TD
    User[User] --> Authentication[Authentication]
    
    Authentication --> Identity[Identity Provider]
    
    Identity --> TenantContext[Tenant Context]
    
    TenantContext --> RoleAssignment[Role Assignment]
    
    RoleAssignment --> Roles[Roles]
    
    Roles --> Permissions[Permissions]
    
    Permissions --> Resources[Resources]
    
    Resources --> PromptTemplates[Prompt Templates]
    Resources --> Providers[LLM Providers]
    Resources --> Configuration[System Configuration]
    Resources --> Analytics[Analytics Data]
```

**Access Control Implementation:**

1. User authentication through identity provider
2. Tenant context establishment
3. Role assignment based on tenant and user
4. Permission checking for operations
5. Resource-level access control

### Auditing and Compliance

The LLM Gateway implements comprehensive auditing for compliance:

```mermaid
graph TD
    Actions[System Actions] --> AuditCapture[Audit Capture]
    
    AuditCapture --> AuditEvents[Audit Events]
    
    AuditEvents --> Storage[Audit Storage]
    
    Storage --> Retention[Retention Policy]
    
    Storage --> AccessControl[Access Control]
    
    Storage --> Reporting[Compliance Reporting]
    
    Storage --> Alerting[Security Alerting]
```

**Auditing Implementation:**

1. Capture of all significant system actions
2. Standardized audit event format
3. Secure, tamper-evident storage
4. Configurable retention policies
5. Access control for audit data
6. Compliance reporting and alerting

## Domain Events

The LLM Gateway uses domain events to communicate between components:

```mermaid
classDiagram
    class DomainEvent {
        <<interface>>
        +String getEventId()
        +String getTenantId()
        +String getUserId()
        +Date getTimestamp()
        +Map~String, Object~ getMetadata()
    }
    
    class PromptCreatedEvent {
        <<event>>
        +String promptId
        +String name
        +String createdBy
    }
    
    class PromptPublishedEvent {
        <<event>>
        +String promptId
        +String version
        +String publishedBy
    }
    
    class ProviderFailureEvent {
        <<event>>
        +String providerType
        +String errorType
        +String errorMessage
    }
    
    class UsageLimitReachedEvent {
        <<event>>
        +String tenantId
        +String limitType
        +long currentUsage
        +long limitValue
    }
    
    DomainEvent <|-- PromptCreatedEvent
    DomainEvent <|-- PromptPublishedEvent
    DomainEvent <|-- ProviderFailureEvent
    DomainEvent <|-- UsageLimitReachedEvent
```

**Event Handling:**

1. Events are published to an event bus
2. Components subscribe to relevant events
3. Events are processed asynchronously
4. Events can trigger system actions or notifications
5. Events are recorded for audit purposes

## Business Rules

The LLM Gateway implements the following key business rules:

1. **Tenant Isolation**
   - Data from one tenant must never be accessible to another tenant
   - Resources must be allocated and tracked per tenant
   - Configuration must be tenant-specific

2. **Provider Management**
   - Provider credentials must be securely stored
   - Provider failures must be handled gracefully
   - Provider selection must follow defined priority and capability rules

3. **Prompt Governance**
   - Prompt templates must follow a version-controlled lifecycle
   - Published prompts must be immutable
   - Prompt usage must be tracked for audit and analytics

4. **Usage Control**
   - Usage limits must be enforced at tenant and user level
   - Usage must be tracked accurately for billing and analytics
   - Rate limiting must prevent abuse and ensure fair resource allocation

5. **Security and Compliance**
   - All actions must be authenticated and authorized
   - Sensitive operations must be audited
   - Compliance requirements must be configurable per tenant

---

**Previous**: [Extension Points and Plug-In Strategy](./extension-points.md) | **Next**: [Deployment and Scaling Architecture](./deployment-scaling.md)