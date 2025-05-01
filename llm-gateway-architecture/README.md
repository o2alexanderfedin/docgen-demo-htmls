# LLM Gateway Documentation

This repository contains comprehensive technical documentation for the LLM Gateway, which serves as the conduit between Aisera services and Large Language Models (LLMs).

## Documentation Contents

- [Architecture & Design Document](./architecture.md) - Comprehensive technical architecture description with 4+1 view diagrams, module breakdowns, and data models.
- [API Reference](./api-reference.md) - Detailed API documentation for REST and gRPC interfaces.
- [Operations Guide](./operations.md) - Deployment, configuration, monitoring, and troubleshooting information.

## Overview

The LLM Gateway is a service that provides a unified interface for Aisera services to interact with various Large Language Models (LLMs), both external (GPT-4, Llama2) and internal (fine-tuned models). It handles prompt management, execution, and caching, offering both REST and gRPC APIs.

## Key Features

- **Prompt Management**: Create, update, and delete prompt templates
- **Execution Management**: Execute LLM requests with unified interface
- **Client Management**: Integrate with multiple LLM providers
- **Caching**: Cache LLM responses for improved performance
- **Analytics**: Collect metrics on LLM usage
- **Multi-tenancy**: Support for multiple tenants with isolation

## Architecture

The LLM Gateway follows a modular architecture based on the open-closed principle:

- **Core Module**: Application bootstrap and configuration
- **Execution Module**: Handles execution of LLM requests
- **Prompt Module**: Manages prompt templates and registry
- **Client Module**: Manages connections to LLM providers
- **REST/gRPC APIs**: External interfaces for service access

See the [Architecture & Design Document](./architecture.md) for detailed information.

## Getting Started

For information on setting up a local development environment for the LLM Gateway, refer to the [Operations Guide](./operations.md#standalone-deployment).

## API Reference

The LLM Gateway provides both REST and gRPC interfaces. See the [API Reference](./api-reference.md) document for detailed information on all available endpoints and methods.

## License

Copyright (c) 2023-2025 Aisera, Inc. All rights reserved.