# Project Overview

## Purpose

This project is a Python-based SIT automation framework for banking/payment API testing. It separates test definitions from code:

- Test selection and expectations live in Excel workbooks.
- Service URLs and API metadata live in YAML files.
- Request bodies live as JSON templates.
- Runtime values are injected through placeholder tokens.

The main entry point is `runner.py`.

## Main Workflow

1. Load YAML configuration from `config/servers.yaml`, `config/apis.yaml`, and `config/test_data.yaml`.
2. Merge service infrastructure settings with service API definitions.
3. Apply optional environment filters such as `ENABLED_SERVICES` and `DISABLED_SERVICES`.
4. Load executable testcase rows from service-specific Excel files.
5. Execute authentication testcases first for each service.
6. Execute independent non-auth testcases in parallel.
7. Execute dependent/sequential testcases in testcase-number order.
8. Render request payloads from JSON templates.
9. Call APIs using retry-enabled HTTP client logic.
10. Validate responses.
11. Write JSON, CSV, HTML reports, and logs.

## Configured Services

| Service | Workbook | Sheet | Request directory | Current status |
| --- | --- | --- | --- | --- |
| `cas` | `testcases/sit_testcases.xlsx` | `SIT` | `requests/cas/` | Primary populated service |
| `acquiring` | `testcases/sit_testcases_acquiring.xlsx` | `ACQUIRING` | `requests/acquiring/` | Configured/scaffolded |
| `merchant_cas` | `testcases/sit_testcases_merchant_cas.xlsx` | `MERCHANT_CAS` | `requests/merchant_cas/` | Configured with sample coverage |

## Key Runtime Outputs

| Directory | Contents |
| --- | --- |
| `results/` | `results_<timestamp>.json` and `results_<timestamp>.csv` |
| `reports/` | `report_<timestamp>.html` |
| `logs/` | Rotating logs for framework, requests, responses, validation, and errors |

## Project Counts At Documentation Time

- JSON request templates: 376
- HTML reports: 57
- JSON result files: 55
- CAS testcase rows: 359 total, 346 enabled
- Acquiring testcase rows: 0
- Merchant CAS testcase rows: 1 enabled

