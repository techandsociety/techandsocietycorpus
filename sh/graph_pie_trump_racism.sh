LABEL_FILE=labels/racism_study3.annotated.json

cat ${LABEL_FILE} | \
python -m jsql/filter query eq "donald trump" | \
# Note: we re-unique the queries, in case there are stories that had duplicate urls.
python -m jsql/select_unique publication+title | \
# Note: 'n' means 'not actually about topic'
python -m jsql/filter ratings.gcop_v1 neq n | \
python -m graph/pie ratings.gcop_v1 legends/trump_racism images/trump_racism_pie.png
