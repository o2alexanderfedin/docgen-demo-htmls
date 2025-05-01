# API Versioning & Deprecation Policy

This document outlines the LLM Gateway API versioning strategy, backward compatibility guarantees, and deprecation policies to help you plan and manage your integration.

## Table of Contents

- [API Versioning Strategy](#api-versioning-strategy)
- [Backward Compatibility](#backward-compatibility)
- [Deprecation Policy](#deprecation-policy)
- [Version Lifecycle](#version-lifecycle)
- [Staying Informed](#staying-informed)
- [Migration Guidelines](#migration-guidelines)

## API Versioning Strategy

The LLM Gateway API uses a date-based versioning scheme combined with semantic versioning principles to manage changes and ensure stability for client applications.

### Version Format

API versions follow this pattern:

```
v{YYYY-MM-DD}
```

Example: `v2023-06-01`

### Version Specification

You can specify which API version to use in one of three ways:

1. **URL Path** (recommended):
   ```
   https://api.aisera.com/v2023-06-01/tenants/{tenantId}/llm/prompts
   ```

2. **Accept Header**:
   ```
   Accept: application/json; version=2023-06-01
   ```

3. **Custom Header**:
   ```
   X-API-Version: 2023-06-01
   ```

If no version is specified, the API will use the latest non-preview version.

### Preview Versions

Preview versions of the API allow early access to new features and are clearly marked:

```
v2023-06-01-preview
```

Preview versions:
- May change without notice
- Do not have backward compatibility guarantees
- Are not recommended for production use

## Backward Compatibility

We maintain backward compatibility within each major API version. This means:

### Guaranteed Compatible Changes

The following changes may be made without incrementing the major version:

- Adding new API endpoints
- Adding new optional request parameters
- Adding new properties to response objects
- Adding new enum values
- Improving error messages
- Performance improvements

### Breaking Changes

The following changes are considered breaking and will only occur with a new major version:

- Removing or renaming API endpoints
- Removing or renaming properties in request or response bodies
- Changing the type of a property
- Adding new required request parameters
- Changing the status code for a particular error condition
- Changing the error code for a particular error condition

## Deprecation Policy

### Notice Period

We provide advance notice before deprecating any API version or feature:

- **Major API versions**: Minimum 12 months notice
- **Individual endpoints**: Minimum 6 months notice
- **Parameters or response fields**: Minimum 3 months notice

### Deprecation Notices

Deprecation notices are communicated through:

1. **Response Headers**:
   ```
   Deprecation: true
   Sunset: Sat, 31 Dec 2023 23:59:59 GMT
   Link: <https://api.aisera.com/v2024-01-01/tenants/{tenantId}/llm/prompts>; rel="successor-version"
   ```

2. **Developer Portal**: All deprecations are documented in the developer portal with migration guides.

3. **Email Notifications**: Registered API users receive email notifications for major deprecations.

### Deprecation Warning Headers

When using a deprecated feature, you will receive the following response headers:

- `Deprecation: true` - Indicates the resource is deprecated
- `Sunset: <date>` - The date after which the resource may no longer be available
- `Link: <uri>; rel="successor-version"` - URI of the replacement resource

## Version Lifecycle

API versions go through the following lifecycle stages:

1. **Preview**: Early access, may change without notice
2. **General Availability (GA)**: Production-ready, backward compatibility guaranteed
3. **Deprecated**: Still available but scheduled for removal
4. **Sunset**: No longer available

### Current Versions

| Version | Status | Sunset Date | Notes |
|---------|--------|-------------|-------|
| v2023-06-01 | GA | N/A | Current stable version |
| v2022-12-01 | Deprecated | 2024-01-01 | Use v2023-06-01 instead |
| v2023-10-01-preview | Preview | N/A | Next version in preview |

## Staying Informed

Stay up to date with API changes through the following channels:

1. **Change Log**: We maintain a detailed change log at `https://api.aisera.com/changelog`

2. **Developer Newsletter**: Subscribe at `https://api.aisera.com/subscribe`

3. **API Status Page**: Check service status at `https://status.aisera.com`

4. **RSS Feed**: Subscribe to the API changes RSS feed at `https://api.aisera.com/changelog.rss`

## Migration Guidelines

### Upgrading Between Versions

Follow these best practices when upgrading to a new API version:

1. **Review the Migration Guide**: Each new API version comes with a comprehensive migration guide outlining all changes.

2. **Test in Sandbox**: Before migrating production code, test thoroughly in the sandbox environment.

3. **Update API Clients**: If you're using our official client libraries, update to the latest version that supports the new API version.

4. **Gradual Rollout**: Consider rolling out the API version update to a small percentage of your users first.

5. **Monitor Error Rates**: After upgrading, closely monitor your application's error rates and performance.

### Automated Compatibility Testing

We provide a compatibility testing tool that you can use to check your application against different API versions:

```bash
curl "https://api.aisera.com/compatibility-check" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "current_version": "v2022-12-01",
    "target_version": "v2023-06-01",
    "endpoints": [
      "/tenants/{tenantId}/llm/prompts",
      "/tenants/{tenantId}/llm/execute"
    ]
  }'
```

This tool will analyze your API usage patterns and identify potential compatibility issues before you migrate.

### Version-Specific Documentation

Documentation for all API versions remains available even after a version is deprecated:

```
https://api.aisera.com/docs/v2022-12-01
```

This allows you to reference previous behavior while migrating to newer versions.