# Module And Script Reference

## Root Files

| File | Purpose |
| --- | --- |
| `runner.py` | Main framework entry point. Loads config/testcases, executes API calls, handles auth, flows, validation, and report writing. |
| `slack_report_alert.py` | Optional watcher for generated HTML reports. Parses report data and posts summaries/files to Slack. |
| `requirements.txt` | Pinned Python runtime dependencies. |
| `README.md` | Entry documentation and links to this docs set. |

## `utils/`

| File | Main objects | Purpose |
| --- | --- | --- |
| `api_client.py` | `ApiClient` | Wraps `requests.Session`, applies retry behavior, logs requests/responses, returns normalized response dictionaries. |
| `data_generator.py` | `DataGenerator` | Generates default runtime tokens: `RRN`, `STAN`, `DATE`, and `TIME`. |
| `logger.py` | `LoggerFactory` | Configures rotating log files and console handlers for framework, request, response, validation, and error logs. |
| `service_manager.py` | `ServiceConfig`, `ServiceManager` | Holds service config, enabled state, base URLs, auth config, API definitions, and token routing. |
| `template_engine.py` | `TemplateEngine` | Loads JSON request templates and recursively replaces `${TOKEN}` placeholders. |
| `__init__.py` | n/a | Package marker. |

## `validators/`

| File | Main objects | Purpose |
| --- | --- | --- |
| `response_validator.py` | `ResponseValidator` | Implements `response`, `json_field`, and `status_code` validation modes. |
| `__init__.py` | n/a | Package marker. |

## `scripts/`

| File | Purpose |
| --- | --- |
| `add_sit_testcases.py` | Appends chained title-fetch/direct-posting testcase rows to the main CAS workbook. |
| `create_sample_excel.py` | Creates a sample generated workbook with example CAS, acquiring, and merchant CAS rows. |
| `create_service_specific_excel.py` | Creates service-specific acquiring and merchant CAS workbook shells. |
| `list_testcases.py` | Prints selected testcase row details from the main workbook. |

## Generated Or Runtime Directories

| Directory | Purpose |
| --- | --- |
| `logs/` | Rotating runtime logs. |
| `reports/` | Generated HTML reports. |
| `results/` | Generated JSON and CSV results. |
| `__pycache__/` | Python bytecode cache. |

## Data Directories

| Directory | Purpose |
| --- | --- |
| `config/` | YAML files for service URLs, API definitions, auth/token behavior, flows, and test data tokens. |
| `requests/` | JSON request templates, grouped by service. |
| `testcases/` | Excel workbooks that control testcase execution. |
| `offline_packages/` | Wheel files for offline dependency installation. |

