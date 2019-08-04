python -m jsql.ingest "$1" | \
python -m jsql.group date  | \
python -m jsql.count

