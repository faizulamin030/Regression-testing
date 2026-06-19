# Execution And Reporting

## Run The Framework

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python runner.py
```

With selected services:

```powershell
$env:ENABLED_SERVICES="cas"
python runner.py
```

With higher parallelism:

```powershell
$env:MAX_WORKERS="8"
python runner.py
```

## What Happens During A Run

1. Config files are loaded.
2. Enabled services are identified.
3. Excel rows marked `Y` are loaded.
4. Auth cases run first for each service.
5. Independent non-auth cases run with `ThreadPoolExecutor`.
6. Sequential cases run in numeric order.
7. Results are sorted by service and testcase ID.
8. Output files are written with a timestamp tag.

## Output Files

Each run creates:

```text
results/results_<YYYYMMDD_HHMMSS>.json
results/results_<YYYYMMDD_HHMMSS>.csv
reports/report_<YYYYMMDD_HHMMSS>.html
```

The HTML report includes:

- Summary metrics.
- Pass/fail status.
- Service grouping.
- Response times.
- Request payloads and headers.
- Response bodies.
- Actual validation output.

## Logs

Logs are written to `logs/` and rotate at 5 MB with 5 backups.

| Log | Contents |
| --- | --- |
| `framework.log` | Run lifecycle, testcase loading, service selection |
| `request.log` | Outgoing method, URL, headers, and payload |
| `response.log` | Status code, elapsed time, and response body |
| `validation.log` | Validation decisions |
| `error.log` | Exceptions and HTTP request failures |

## Slack Report Watcher

`slack_report_alert.py` watches the `reports/` directory for generated HTML reports, parses report summary data, builds a Slack message, optionally creates an analytics chart, and uploads or posts report details.

Run it separately from the test runner:

```powershell
python slack_report_alert.py
```

Before using it, move secrets and environment-specific settings out of the source file. See `docs/OPERATIONS_SECURITY.md`.

## Troubleshooting

If a testcase fails before sending the request:

- Check `API_Name` exists in `config/apis.yaml`.
- Check `Request_File` exists under `requests/<service>/`.
- Check the Excel row has all required columns.
- Check the selected service is enabled.

If an API returns unauthorized:

- Confirm the auth testcase ran first.
- Confirm `auth.token_json_path` matches the auth response body.
- Confirm `token_routing` maps the API to the same channel captured from the auth request file.

If validation fails unexpectedly:

- Use the HTML report to compare expected and actual values.
- Check `Validation_Type`.
- For `json_field`, verify the JSON path and the exact string value.

