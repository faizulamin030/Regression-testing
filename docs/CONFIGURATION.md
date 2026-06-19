# Configuration Guide

## `config/servers.yaml`

Defines service infrastructure and legacy bank mappings.

Service fields:

| Field | Meaning |
| --- | --- |
| `enabled` | Whether the service runs by default |
| `display_name` | Human-readable name used in logs/reports |
| `base_url` | Service base URL |

Legacy `banks` entries can map a bank name to a service and/or base URL. The current runner prefers the service base URL when available.

## `config/apis.yaml`

Defines runtime defaults, service-scoped APIs, authentication, token routing, and flows.

Top-level `defaults`:

| Field | Meaning |
| --- | --- |
| `timeout_seconds` | HTTP timeout per request |
| `retries` | Retry count for retryable failures |
| `retry_backoff_factor` | Backoff multiplier used by urllib3 retry logic |
| `retry_status_codes` | HTTP status codes that should be retried |

Service config structure:

```yaml
services:
  cas:
    display_name: "CAS Service"
    auth:
      apis:
        - authenticate
      token_json_path: token
    token_routing:
      payment: ib
    apis:
      payment:
        endpoint: /api/v1/example/payment
        method: POST
        headers:
          Content-Type: application/json
```

API fields:

| Field | Required | Meaning |
| --- | --- | --- |
| `endpoint` | Yes | Path appended to the service base URL |
| `method` | Yes | HTTP method |
| `headers` | No | Base request headers before bearer token injection |

## `config/test_data.yaml`

Defines user-controlled tokens used by request templates. Keys are uppercased by the runner, so a key like `receiver_iban` becomes `${RECEIVER_IBAN}`.

Do not place production secrets here. The file is loaded at runtime and its values can appear in request logs, result JSON, CSV files, and HTML reports.

## `config/reporting.yaml`

Controls generated report defaults.

```yaml
html_report:
  hide_sensitive_data: true
  show_failure_analysis: true
  show_details: true
```

| Field | Meaning |
| --- | --- |
| `hide_sensitive_data` | Redacts sensitive values in HTML reports only. JSON and CSV results remain raw. |
| `show_failure_analysis` | Shows the Failure Analysis section by default when a report is opened. |
| `show_details` | Shows the API request/response detail section by default when a report is opened. |

The HTML report still includes buttons to show or hide analysis and details after opening. Browser storage may remember the viewer's last choice.

## Environment Variables

| Variable | Example | Effect |
| --- | --- | --- |
| `MAX_WORKERS` | `8` | Controls parallel worker count for independent testcases |
| `ENABLED_SERVICES` | `cas,merchant_cas` | Enables only the listed services |
| `DISABLED_SERVICES` | `acquiring` | Disables listed services after normal config loading |

PowerShell example:

```powershell
$env:MAX_WORKERS="8"
$env:ENABLED_SERVICES="cas"
python runner.py
```

## Adding A New API

1. Add the API under the correct service in `config/apis.yaml`.
2. Add token routing if the endpoint requires a specific auth channel.
3. Create a JSON request template in `requests/<service>/`.
4. Add a testcase row to the service workbook.
5. Run `python runner.py` and inspect `logs/error.log` and the generated report.

## Adding A New Service

1. Add service infrastructure to `config/servers.yaml`.
2. Add service API definitions to `config/apis.yaml`.
3. Create `requests/<service>/`.
4. Add a workbook source in `runner.py` if the service needs its own Excel file.
5. Add testcase rows and run with `ENABLED_SERVICES=<service>` during initial testing.
