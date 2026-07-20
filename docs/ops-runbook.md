# Operations Runbook

## Local development

```bash
docker compose up --build
curl -H "X-API-Key: dev-api-key" -X POST http://localhost:8000/v1/scans \
  -H "Content-Type: application/json" \
  -d '{"url":"http://example.com/login"}'
```

Run migrations:

```bash
alembic upgrade head
```

## Health checks

- `GET /healthz` — process liveness
- `GET /readyz` — database connectivity

## Deployment

Production image:

```bash
docker build --target prod -t arkana-api:latest .
```

Production compose profile:

```bash
docker compose --profile prod up --build -d
```

## Incident handling

### Database unavailable

Symptoms: `/readyz` returns 503, scan creation fails with 503.

Actions:
1. Verify Postgres is running and reachable.
2. Check `DATABASE_URL` configuration.
3. Restart API after database recovery.

### Scan failures

Symptoms: scans stuck in `failed` or `partial`.

Actions:
1. Inspect structured logs for `scan_id`, `stage_timings`, and `fetch_error`.
2. Verify outbound network access for HTTP/DNS/RDAP.
3. Check rate limits and blocked target IPs (SSRF protection).

### Campaign merge review

Symptoms: `merge_review_events` rows or log warnings with `multiple_candidate_campaigns`.

Actions:
1. Review candidate campaign IDs in the event row.
2. Validate whether scans should share a campaign based on link evidence.
3. Manual merge/split workflows are post-v1.

## Rollback

1. Stop API containers.
2. Roll back database migration if needed: `alembic downgrade -1`
3. Deploy previous image tag.
4. Verify `/readyz` and submit a test scan.

## Load testing

```bash
python scripts/load_test.py --url http://localhost:8000 --api-key dev-api-key --requests 20
```
