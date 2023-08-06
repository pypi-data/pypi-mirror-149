# Changelog

## 0.0.12 - 2022-05-06

* Improved the file checker to detect repeated quotes in CSV.

## 0.0.11 - 2022-05-02

* Fix import error in `file_checker` script

## 0.0.10 - 2022-04-27

* Snowflake: discard 11 more `query_type` values when fetching queries

## 0.0.9 - 2022-04-13

* allow Looker parameters `CASTOR_LOOKER_TIMEOUT_SECOND` and `CASTOR_LOOKER_PAGE_SIZE` to be passed through environment
variables
* fix import paths in `castor_extractor/commands/upload.py` script
* use `storage.Client.from_service_account_info` when `credentials` is a dictionary in `uploader/upload.py`

## 0.0.8 - 2022-04-07
Fix links to documentation in the README

## 0.0.7 - 2022-04-05
Fix dateutil import issue

## 0.0.6 - 2022-04-05

First version of Castor Extractor, including:

- Warehouse assets extraction
  - BigQuery
  - Postgres
  - Redshift
  - Snowflake

- Visualization assets extraction
  - Looker
  - Metabase
  - Mode Analytics
  - Tableau

- Utilities
  - Uploader to cloud-storage
  - File Checker (for generic metadata)
