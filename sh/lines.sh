python -m db.tojson "$1" | \
# python -m jsql.ingest "$1" | \
python -m jsql.group date  | \
python -m jsql.collapse publication | \
python -m graph.lines

