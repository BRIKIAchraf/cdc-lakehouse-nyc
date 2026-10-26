# CDC Lakehouse NYC

Portfolio architecture for a change-data-capture and analytics platform built around New York City taxi data.

## Objective

Create a replayable data platform that can ingest historical NYC TLC files, capture source changes and publish trusted analytical datasets.

## Target architecture

~~~text
NYC TLC Parquet → Python replay loader → PostgreSQL
                                      ↓
                              Debezium CDC
                                      ↓
                                    Kafka
                                      ↓
                         Spark Structured Streaming
                                      ↓
                              Apache Hudi on S3
                                      ↓
                            Snowflake → dbt marts
~~~

Open-Meteo weather data is planned as an enrichment source through Airbyte. Data quality, lineage and monitoring are treated as first-class concerns.

## Data layers

| Layer | Grain | Purpose |
|---|---|---|
| Bronze | One CDC event | Append-only source payload and replay |
| Silver | One current trip | Canonical schema, deduplication and upsert |
| Gold | Trip or hourly aggregate | Certified measures for analytics |

## Engineering principles

- replayable ingestion and controlled reprocessing;
- idempotent upserts using business and technical keys;
- versioned event contracts and backward-compatible evolution;
- checks for uniqueness, timestamps, geographic bounds and business rules;
- Kafka lag, freshness, rejected records and processing-time metrics;
- secrets outside Git and least-privilege access.

## Planned repository layout

~~~text
src/ingestion/       Historical replay and source loading
src/streaming/       Spark CDC processing and Hudi upserts
src/enrichment/      Weather enrichment
dbt/                 Staging, intermediate and mart models
infra/               Docker, Terraform and service configuration
docs/                Architecture and operating decisions
~~~

## Status

**Blueprint in active implementation.** The architecture and data contracts are documented; execution jobs, integration tests and deployment manifests are being added incrementally.

## Roadmap

- [ ] Add local PostgreSQL, Kafka, Debezium and object storage stack.
- [ ] Implement NYC TLC replay with schema validation.
- [ ] Add CDC contracts and consumer tests.
- [ ] Implement Spark streaming and Hudi upserts.
- [ ] Add dbt models, data-quality checks and observability.
- [ ] Add CI, secret scanning and cloud deployment documentation.

## Author

**Achraf BRIKI** · [LinkedIn](https://www.linkedin.com/in/achrafbriki/) · [Portfolio](https://achrafbriki.com)
