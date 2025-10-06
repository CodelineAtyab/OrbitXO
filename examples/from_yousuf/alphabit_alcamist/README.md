# String Processor API

Small FastAPI app that converts input strings into a list of numbers according to a compact set of rules. The project includes a MySQL-backed logging helper and a Docker Compose setup to run the API + DB.

## What the app does (rules)
- Each letter a..z maps to 1..26 (case-insensitive). All other characters count as value 0 and become a standalone 0 in the output.
- A leading chain of one-or-more `z` characters is used to build a "count": each `z` adds 26, then the next character (if present) adds its letter value. Example: `zz a` → count = 26 + 26 + 1 = 53.
- After the count is determined, the app collects that many "items". Each item is either:
	- a single character (e.g. `b`), or
	- a z-chain item (one-or-more `z` characters followed by the terminating character). A z-chain is treated as a single item when counting.
- The numeric value for an output element is the sum of letter values of all characters that were collected for that element (z contributes 26 when present). Non-letters contribute 0 but are still included when collected.

## Endpoint
- GET /convert-measurements?input=YOUR_STRING

Response JSON: {"input_string": "...", "output": [numbers]}

## Example (specific test string)
- Test string: `zzabzc`
- Explanation: leading `zz` → 26 + 26, next char `a` adds 1 → count = 53. The app then collects items until the input is exhausted: items collected are `b` and the z-chain `zc` (counts as one item). Values: b=2, z=26, c=3 → sum = 31.
- Expected response:

```
{"input_string":"zzabzc","output":[31]}
```

## Run with Docker Compose (short)
1. Build and start services (API on :8080, MySQL on :3306):

```powershell
docker compose up --build -d
```

2. Wait until the `db` service is healthy, then call the endpoint. Example using PowerShell:

```powershell
Invoke-RestMethod -Uri "http://localhost:8080/convert-measurements?input=zzabzc" -Method GET | ConvertTo-Json
```

To view service logs:

```powershell
docker compose logs -f app
```

That's it — the API will also attempt to log requests to MySQL (see `docker-compose.yml` for DB env variables). If DB logging fails the project writes a fallback JSONL in the project directory.

