VERSION=3

LABEL_FILE=labels/racism_study${VERSION}.annotated.json

cat ${LABEL_FILE} | \
python -m jsql/filter query eq "donald trump" | \
# Note: 'n' means 'not actually about racism'
python -m jsql/filter ratings.gcop_v1 neq n | \
python -m graph/pie ratings.gcop_v1 legends/trump_racism
