# Operations And Security Notes

## Sensitive Data

This project contains environment-specific URLs, request payloads, logs, reports, and test data. Treat the repository and generated artifacts as internal.

Be careful with:

- `config/test_data.yaml`
- JSON templates under `requests/`
- Generated files under `results/`, `reports/`, and `logs/`
- Slack settings in `slack_report_alert.py`

## Hardcoded Slack Token

`slack_report_alert.py` currently contains a hardcoded Slack bot token and channel ID. This should be rotated and moved to environment variables before the watcher is used beyond a local/internal environment.

Recommended environment-variable pattern:

```powershell
$env:SLACK_BOT_TOKEN="xoxb-..."
$env:SLACK_CHANNEL_ID="C..."
python slack_report_alert.py
```

Then update the script to read from `os.getenv()`.

## Log And Report Exposure

The API client logs request headers, payloads, response bodies, and errors. Generated reports also include request and response details. If payloads contain account identifiers, CNICs, mobile numbers, tokens, or API secrets, those values can be copied into artifacts.

Recommended practices:

- Do not share generated reports externally without review.
- Periodically clean old `results/`, `reports/`, and `logs/` artifacts.
- Avoid using production customer data.
- Mask authorization headers and sensitive payload fields before broad distribution.

## Dependency Management

Python dependencies are pinned in `requirements.txt`:

- `requests`
- `PyYAML`
- `openpyxl`

There is also an `offline_packages/` directory containing wheel files for offline installation. Keep those wheels aligned with `requirements.txt` when dependencies change.

## Runtime Reliability

The HTTP client uses retry logic for common transient status codes such as 408, 429, and 5xx responses. Tune retry behavior in `config/apis.yaml` under `defaults`.

Use a smaller `MAX_WORKERS` when:

- Target services throttle requests.
- Auth/token state is unstable.
- You are debugging failures.

Use service filtering during development:

```powershell
$env:ENABLED_SERVICES="cas"
python runner.py
```

