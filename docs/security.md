# Security

## Scope

This project is a local development demo intended to illustrate Kafka-based event-driven communication.

It is not production hardened.

## Current security posture

The current implementation intentionally favors simplicity over hardening.

### Kafka
- no TLS
- no SASL authentication
- single local broker
- plain text local communication

### Kafka UI
- exposed without authentication
- intended for local development only

### Application layer
- no user authentication
- no authorization model
- no secret manager integration
- no payload signature or encryption
- no schema enforcement at runtime

## Risks in the current form

If this project were exposed outside a trusted local environment, the main concerns would be:

- unauthorized access to Kafka
- unauthorized access to Kafka UI
- unvalidated payloads entering the system
- lack of encryption in transit
- weak auditability

## Recommendations for a production-grade version

### Transport security
- enable TLS for Kafka broker traffic
- enable TLS for all producer/consumer clients

### Authentication and authorization
- enable SASL for Kafka clients
- restrict topic access with ACLs
- protect Kafka UI behind authentication

### Event validation
- validate payloads against a schema before publishing
- reject invalid or incomplete messages

### Secrets and configuration
- move sensitive configuration to a secret store
- avoid embedding environment-specific credentials in source code

### Observability and audit
- use structured logs
- add correlation ids
- add producer / consumer metrics
- retain audit trails for operational debugging

## Practical interview note

One of the strengths of this project is that it gives a clear platform to discuss the difference between:

- a local developer demo
- a production-ready event platform

That distinction is often more valuable in interviews than pretending a small demo is already production hardened.