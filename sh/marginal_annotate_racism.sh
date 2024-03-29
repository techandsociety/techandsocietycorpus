VERSION=3

RAW_FILE=labels/racism_study${VERSION}.json
LABEL_FILE=labels/racism_study${VERSION}.annotated.json
touch $LABEL_FILE
# python -m pipeline.make_json_datasets
python -m jsql.ensure_json ${LABEL_FILE}
python -m studies.compute_keyword_study ${RAW_FILE} racism trump
python -m tools.label_json ${RAW_FILE} ${LABEL_FILE} gcop_v1 legends/trump_racism
