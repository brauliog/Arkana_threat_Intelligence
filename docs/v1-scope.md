# Arkana v1 Scope

This document defines what is in scope for Arkana v1 delivery. The README describes the long-term product vision; v1 follows the engineering design doc.

## In scope

- URL submission and async scan lifecycle (`POST /v1/scans`, `GET /v1/scans/{id}`)
- Bounded HTTP fetch, DNS resolution, and RDAP domain metadata
- Deterministic signal extraction and versioned scoring
- Campaign correlation via persisted scan links (no graph database)
- Campaign detail endpoint (`GET /v1/campaigns/{id}`)
- API key authentication stub
- Health endpoints, structured logging, CI, and Docker packaging

## Out of scope for v1

- Machine learning classification
- Real-time streaming or event-driven ingestion
- External threat intelligence feeds in the critical path
- Frontend UI
- Multi-tenant isolation
- Graph database infrastructure
- TLS certificate analysis
- OAuth/JWT (planned; API key stub ships in v1)

## API contract note

v1 uses async polling: `POST /v1/scans` returns `202 Accepted` with `scan_id` and `status=queued`. Clients poll `GET /v1/scans/{scan_id}` until the scan reaches a terminal state.
