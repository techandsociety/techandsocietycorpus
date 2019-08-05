VERSION=1

RAW_FILE=labels/mueller_study${VERSION}.json
LABEL_FILE=labels/mueller_study${VERSION}.annotated.json
touch $LABEL_FILE
python -m jsql.ensure_json ${LABEL_FILE}
python -m studies.compute_keyword_study ${RAW_FILE} mueller trump
python -m tools.label_json ${RAW_FILE} ${LABEL_FILE} gcop_v1 legends/trump_mueller
