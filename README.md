# Customer Segmentation & AI Insights — Interview Bundle

This bundle contains **demonstration assets** that mirror a real VoC + churn project, suitable for portfolio/interview use.

## Contents
- `data/synthetic_customers.csv` — synthetic dataset for demos
- `etl_churn_model.py` — ETL + training + scoring (sklearn pipeline)
- `airflow_dag.py` — example Airflow DAG (daily schedule)
- `voc_churn_analysis.Rmd` — R Markdown for VoC sentiment/themes
- `out/` — model outputs (e.g., `churn_scores.csv`)
- `tableau/README_Tableau.md` — how to build the dashboards
- `requirements.txt` — Python dependencies

## Quickstart (Python)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python etl_churn_model.py
# Outputs: models/churn_logit_pipeline.joblib, out/churn_scores.csv
```

## Quickstart (R)
Open `voc_churn_analysis.Rmd` in RStudio → Knit to HTML.

## Airflow
- Place `airflow_dag.py` in your DAGs folder.
- Update the `bash_command` paths to your repo.
- DAG: daily 03:00 UTC — ETL/train/score → copy CSV to Tableau drop.

## Tableau
- Connect to `out/churn_scores.csv` as data source.
- Build the KPI/segment/journey sheets as noted in `tableau/README_Tableau.md`.
- Optional: Join with VoC theme counts exported from R.

## Notes for Interviewers
- All data is synthetic and privacy-safe.
- The code demonstrates structure and best practices for a churn & VoC workflow.
